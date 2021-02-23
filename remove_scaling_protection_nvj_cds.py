#! /usr/bin/python

import boto3
import json

session = boto3.Session()
client = session.client('autoscaling', region_name='eu-west-1')
ASG_list = ['prd-nvj-sc9-sccd',
            'prd-hcp-sc9-sccd',
            'prd-glo-sc9-sccm',
            'prd-glo-sc9-scxc',
            'prd-glo-sc9-scdd',
            'prd-glo-sc9-proc']
for ASG in ASG_list:
    response = client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[
            ASG,
        ],
    )

    instances = response['AutoScalingGroups'][0]['Instances']


    for i in range(len(instances)):
        instance_id = instances[i]['InstanceId']
        response = client.set_instance_protection(
        AutoScalingGroupName=ASG,
        InstanceIds=[
            instance_id,
        ],
        ProtectedFromScaleIn=False,
        )
        print('scale-in protection removed from: ' + ASG + ' ' + instance_id)
