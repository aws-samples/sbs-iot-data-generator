# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import random
import datetime
import boto3
import time
import logging
from botocore.exceptions import ClientError
from argparse import ArgumentParser
import uuid

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('iot_data_generator.log')
    ]
)
logger = logging.getLogger(__name__)

class IoTDataGenerator:
    def __init__(self, region='us-west-2', enable_sending=False):
        self.deviceNames = ['SBS01', 'SBS02', 'SBS03', 'SBS04', 'SBS05']
        self.region = region
        self.enable_sending = enable_sending
        self.iot_client = None
        self.message_counter = 0
        self.session_id = str(uuid.uuid4())
        self.start_time = datetime.datetime.now()
        
    def connect_to_iot(self):
        """Establish connection to IoT Core"""
        try:
            self.iot_client = boto3.client('iot-data', region_name=self.region)
            logger.info(f"Successfully connected to IoT Core in region {self.region}")
            logger.info(f"Session ID: {self.session_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to IoT Core: {str(e)}")
            return False

    def generate_data(self, parameter, min_value, max_value):
        """Generic data generator function"""
        message_id = f"{self.session_id}-{self.message_counter}"
        data = {
            'deviceValue': random.randint(min_value, max_value),
            'deviceParameter': parameter,
            'deviceId': random.choice(self.deviceNames),
            'dateTime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'messageId': message_id,
            'sessionId': self.session_id
        }
        return data

    def log_message_metrics(self):
        """Log message sending metrics"""
        current_time = datetime.datetime.now()
        duration = (current_time - self.start_time).total_seconds()
        messages_per_second = self.message_counter / duration if duration > 0 else 0
        
        logger.info(f"""
Message Metrics:
--------------
Total Messages: {self.message_counter}
Running Time: {duration:.2f} seconds
Messages/Second: {messages_per_second:.2f}
Session ID: {self.session_id}
        """)

    def publish_data(self, topic, data):
        """Publish data to IoT Core topic"""
        if not self.enable_sending:
            logger.info(f"Simulation mode - Would publish to topic {topic}: {data}")
            self.message_counter += 1
            if self.message_counter % 100 == 0:
                self.log_message_metrics()
            return True
        
        try:
            start_time = time.time()
            response = self.iot_client.publish(
                topic=topic,
                payload=json.dumps(data)
            )
            end_time = time.time()
            latency = (end_time - start_time) * 1000  # Convert to milliseconds
            
            self.message_counter += 1
            
            logger.info(f"""
Message Sent:
-----------
Topic: {topic}
Message ID: {data['messageId']}
Device ID: {data['deviceId']}
Parameter: {data['deviceParameter']}
Value: {data['deviceValue']}
Latency: {latency:.2f}ms
            """)

            if self.message_counter % 100 == 0:
                self.log_message_metrics()
            
            return True
        except ClientError as e:
            logger.error(f"""
Publishing Error:
--------------
Topic: {topic}
Message ID: {data['messageId']}
Error: {str(e)}
            """)
            return False

    def generate_and_publish(self):
        """Generate and publish data based on random distribution"""
        parameter_configs = {
            'flow': {
                'probability': (0, 0.20),
                'range': (60, 100),
                'topic': '/sbs/devicedata/flow'
            },
            'temperature': {
                'probability': (0.20, 0.55),
                'range': (15, 35),
                'topic': '/sbs/devicedata/temperature'
            },
            'humidity': {
                'probability': (0.55, 0.70),
                'range': (50, 90),
                'topic': '/sbs/devicedata/humidity'
            },
            'sound': {
                'probability': (0.70, 1.0),
                'range': (100, 140),
                'topic': '/sbs/devicedata/sound'
            }
        }

        rnd = random.random()
        for param, config in parameter_configs.items():
            prob_min, prob_max = config['probability']
            if prob_min <= rnd < prob_max:
                data = self.generate_data(
                    param.capitalize(),
                    config['range'][0],
                    config['range'][1]
                )
                self.publish_data(config['topic'], data)
                return

def main():
    parser = ArgumentParser(description='IoT Data Generator')
    parser.add_argument('--region', default='us-west-2',
                        help='AWS region for IoT Core')
    parser.add_argument('--send', action='store_true',
                        help='Enable actual sending to IoT Core')
    parser.add_argument('--interval', type=float, default=1.0,
                        help='Interval between messages in seconds')
    parser.add_argument('--log-file', default='iot_data_generator.log',
                        help='Log file path')
    
    args = parser.parse_args()

    generator = IoTDataGenerator(region=args.region, enable_sending=args.send)
    
    if args.send and not generator.connect_to_iot():
        logger.error("Failed to initialize IoT Core connection. Exiting.")
        return

    logger.info(f"""
Starting IoT Data Generator:
------------------------
Mode: {'Sending to IoT Core' if args.send else 'Simulation'}
Region: {args.region}
Interval: {args.interval} seconds
Log File: {args.log_file}
    """)
    
    try:
        while True:
            generator.generate_and_publish()
            time.sleep(args.interval)
    except KeyboardInterrupt:
        logger.info("Stopping data generation")
        generator.log_message_metrics()
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        generator.log_message_metrics()

if __name__ == "__main__":
    main()
