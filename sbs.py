# Copyright 2017-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# Licensed under the Amazon Software License (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at
# http://aws.amazon.com/asl/
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions and limitations under the License. 

# Script to generate simulated IoT device parameters data

import json
import random
import datetime
import boto3
import time

deviceNames = ['SBS01', 'SBS02', 'SBS03', 'SBS04', 'SBS05']

iot = boto3.client('iot-data');

# generate Flow values
def getFlowValues():
    data = {}
    data['deviceValue'] = random.randint(60, 100)
    data['deviceParameter'] = 'Flow'
    data['deviceId'] = random.choice(deviceNames)
    data['dateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return data

# generate Temperature values
def getTemperatureValues():
    data = {}
    data['deviceValue'] = random.randint(15, 35)
    data['deviceParameter'] = 'Temperature'
    data['deviceId'] = random.choice(deviceNames)
    data['dateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return data

# generate Humidity values
def getHumidityValues():
    data = {}
    data['deviceValue'] = random.randint(50, 90)
    data['deviceParameter'] = 'Humidity'
    data['deviceId'] = random.choice(deviceNames)
    data['dateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return data

# generate Sound values
def getSoundValues():
    data = {}
    data['deviceValue'] = random.randint(100, 140)
    data['deviceParameter'] = 'Sound'
    data['deviceId'] = random.choice(deviceNames)
    data['dateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return data

# Generate each parameter's data input in varying proportions
while True:
    time.sleep(1)
    rnd = random.random()
    if (0 <= rnd < 0.20):
        data = json.dumps(getFlowValues())
        print data
        response = iot.publish(
             topic='/sbs/devicedata/flow',
             payload=data
        ) 
    elif (0.20<= rnd < 0.55):
        data = json.dumps(getTemperatureValues())
        print data
        response = iot.publish(
             topic='/sbs/devicedata/temperature',
             payload=data
        )
    elif (0.55<= rnd < 0.70):
        data = json.dumps(getHumidityValues())
        print data
        response = iot.publish(
             topic='/sbs/devicedata/humidity',
             payload=data
        )
    else:
        data = json.dumps(getSoundValues())
        print data
        response = iot.publish(
             topic='/sbs/devicedata/sound',
             payload=data     
)