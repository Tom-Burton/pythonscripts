#! /usr/bin/python
import boto3
import sys

session = boto3.Session(profile_name='pon-ecom')
client = session.client('route53',region_name='eu-west-1')

maintenance_values = [
["audi-prd.pon-ecom.lukkien.com","d1kssh4icoxalg.cloudfront.net"," Z3NP2F4GRUT4Q9", "A"],
["skoda-prd.pon-ecom.lukkien.com","d1vuugjkx115a7.cloudfront.net","Z3NP2F4GRUT4Q9", "A"],
["seat-prd.pon-ecom.lukkien.com","d3iau60ecqmvzd.cloudfront.net","Z3NP2F4GRUT4Q9", "A"],
["porsche-prd.pon-ecom.lukkien.com","d1o1nnpbg1gj1.cloudfront.net","Z3NP2F4GRUT4Q9", "A"],
["vw-prd.pon-ecom.lukkien.com","d2u775l3ggtfv1.cloudfront.net","Z3NP2F4GRUT4Q9", "A"],
["vwb-prd.pon-ecom.lukkien.com","d1tlhk71a51109.cloudfront.net","Z3NP2F4GRUT4Q9", "A"],
]


live_values = [
["audi-prd.pon-ecom.lukkien.com","ecom-prd-public-89249099.eu-central-1.elb.amazonaws.com.","Z3NP2F4GRUT4Q9", "A"],
["skoda-prd.pon-ecom.lukkien.com","ecom-prd-public-89249099.eu-central-1.elb.amazonaws.com.","Z3NP2F4GRUT4Q9", "A"],
["seat-prd.pon-ecom.lukkien.com","ecom-prd-public-89249099.eu-central-1.elb.amazonaws.com.","Z3NP2F4GRUT4Q9", "A"],
["porsche-prd.pon-ecom.lukkien.com","ecom-prd-public-89249099.eu-central-1.elb.amazonaws.com.","Z3NP2F4GRUT4Q9", "A"],
["vw-prd.pon-ecom.lukkien.com","ecom-prd-public-89249099.eu-central-1.elb.amazonaws.com.","Z3NP2F4GRUT4Q9", "A"],
["vwb-prd.pon-ecom.lukkien.com","ecom-prd-public-89249099.eu-central-1.elb.amazonaws.com.","Z3NP2F4GRUT4Q9", "A"],
]


def upsert_sitedown_record(name, endpoint, zoneid, recordtype):
    response = client.change_resource_record_sets(
        HostedZoneId=zoneid,
        ChangeBatch={
            'Comment': 'update record for maintenance',
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': name,
                        'Type': recordtype,
                        'AliasTarget': {
                            'HostedZoneId': 'Z2FDTNDATAQYW2',
                            'DNSName': endpoint,
                            'EvaluateTargetHealth': True
                        },
                    }
                },
            ]
        }
    )

def upsert_live_record(name, endpoint, zoneid, recordtype):
    response = client.change_resource_record_sets(
        HostedZoneId=zoneid,
        ChangeBatch={
            'Comment': 'update record for maintenance',
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': name,
                        'Type': recordtype,
                        'AliasTarget': {
                            'HostedZoneId': 'Z215JYRZR1TBD5',
                            'DNSName': endpoint,
                            'EvaluateTargetHealth': True
                        },
                    }
                },
            ]
        }
    )

if sys.argv[1] == "down":
    for entry in maintenance_values:
        upsert_sitedown_record(entry[0],entry[1],entry[2],entry[3])
elif sys.argv[1] == "up":
        for entry in live_values:
            upsert_live_record(entry[0],entry[1],entry[2],entry[3])
else:
    print("enter 'up' or 'down' as first argument")
