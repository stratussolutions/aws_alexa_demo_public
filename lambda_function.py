from __future__ import print_function

import json
import boto3
import botocore
import datetime
import time

def lambda_handler(event, context):

    ec2 = boto3.client('ec2')
    ec2_resource = boto3.resource('ec2')
    sns = boto3.client('sns')
    
    instance_id = None
    while (instance_id == None):
        instances = ec2_resource.instances.filter(
            #Update the filter with your web server name
            Filters=[{'Name': 'tag:Name', 'Values': ['apee-webserver02']}])
        for instance in instances:
            instance_id=instance.id

    ec2.create_image(
        InstanceId=instance_id,
        Name='websrv-quarantine',
        NoReboot=True
    )

    ami_id = None
    while (ami_id == None):
        images = ec2_resource.images.filter(
            Filters=[{'Name': 'name', 'Values': ['websrv-quarantine']}])
        for image in images:
            ami_id=image.id
            ami_state=image.state
        
    ec2.stop_instances(
        InstanceIds=[
                instance_id
        ],
    )
    
    while (ami_state != 'available'):
        time.sleep( 1 )

    ec2_resource.create_instances(
        ImageId=ami_id,
        MinCount=1,
        MaxCount=1,
        KeyName='stratus-demo',
        SecurityGroupIds=['sg-675ed61c'],
        InstanceType='t2.micro',
        SubnetId='subnet-4d08393b',
        InstanceInitiatedShutdownBehavior='stop',
    )
    
    instance_state = None
    while (instance_state == None):
        instances = ec2_resource.instances.filter(
            Filters=[{'Name': 'image-id', 'Values': [ami_id]}])
        for instance in instances:
            instance_state=instance.state
        
    while (instance_state == 'pending'):
        time.sleep( 1 )

    ec2.deregister_image(
        ImageId=ami_id
    )
