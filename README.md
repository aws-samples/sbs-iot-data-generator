# AWS IoT Simple Beer Service Data Generator

This enhanced version of the Simple Beer Service (SBS) data generator creates and publishes simulated IoT device data to AWS IoT Core. The script provides both simulation and actual publishing capabilities with comprehensive logging and monitoring.

## Features

- Simulated data generation for Flow, Temperature, Humidity, and Sound parameters
- Real-time publishing to AWS IoT Core
- Detailed logging of messages and metrics
- Session tracking and message identification
- Performance monitoring and statistics
- Support for both simulation and production modes

## Prerequisites

* Amazon Web Services account
* [AWS Command Line Interface (CLI)](https://aws.amazon.com/cli/)
* Python 3.x
* virtualenv
* Appropriate IAM permissions for AWS IoT Core

## Setup

1. Create a virtual environment:
```sh
python3 -m virtualenv .venv
```

2. Activate the virtual environment:
```sh
# macOS and Linux
source .venv/bin/activate

# Windows
.\.venv\Scripts\activate
```

3. Install dependencies:
```sh
pip install -r requirements.txt
```

## Configuration

Before running the script in sending mode, ensure:
1. AWS credentials are configured (`aws configure`)
2. IoT Core policies and endpoints are set up
3. Your IAM user/role has appropriate IoT Core permissions

## Running the Script

### Simulation Mode
```sh
python sbs.py
```

### Production Mode
```sh
python sbs.py --send --region us-west-2 --interval 1.0
```

### Command Line Arguments
- `--region`: AWS region (default: us-west-2)
- `--send`: Enable actual sending to IoT Core
- `--interval`: Time between messages in seconds (default: 1.0)
- `--log-file`: Custom log file path

## Monitoring Messages in AWS IoT Core Console

To view the messages being published:

1. Open the AWS IoT Core Console
2. Navigate to "Test" (MQTT test client)
3. Click on "Subscribe to a topic"
4. Enter one of the following topics:
   - `/sbs/devicedata/flow`
   - `/sbs/devicedata/temperature`
   - `/sbs/devicedata/humidity`
   - `/sbs/devicedata/sound`
5. Click "Subscribe"

You can subscribe to multiple topics simultaneously by repeating steps 3-5.

## Message Format

Sample message format:
```json
{
    "deviceValue": 75,
    "deviceParameter": "Temperature",
    "deviceId": "SBS03",
    "dateTime": "2025-03-25 14:30:45",
    "messageId": "session-uuid-123",
    "sessionId": "uuid-123"
}
```

## Running on Amazon EC2

1. Create an IAM role with AWSIoTFullAccess policy
2. Launch EC2 instance with the IAM role
3. Connect to the instance:
```sh
sudo su
aws configure  # Set region and output format
```

4. Install requirements:
```sh
pip install boto3
```

5. Upload and run the script:
```sh
python sbs.py --send
```

## Logging

The script logs to both console and file:
- Message details
- Publishing metrics
- Error information
- Session statistics

Metrics logged include:
- Total messages sent
- Messages per second
- Session duration
- Publishing latency

## Troubleshooting

If you encounter connection issues:
1. Verify AWS credentials are properly configured
2. Ensure IAM permissions are correct
3. Check the log file for detailed error messages
4. Verify your IoT Core endpoint is accessible
5. Confirm your region setting matches your IoT Core setup

## Contributing

Feel free to submit issues and enhancement requests!

## License

Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0