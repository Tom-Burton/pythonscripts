#! /usr/bin/python
import boto3
import sys

session = boto3.Session(profile_name='nutricia')
client = session.client('route53',region_name='eu-west-1')

maintenance_values = [
["nutriciavoorjou.nl","213.154.235.236","Z3RMNR1WP46MJP", "A"],
["www.nutriciavoorjou.nl","213.154.235.236","Z3RMNR1WP46MJP", "A"],
["nutriciababy.be","213.154.235.236","Z5QC0VW6FH4AT", "A"],
["www.nutriciababy.be","213.154.235.236","Z5QC0VW6FH4AT", "A"],
["hcp-sc9.nutricianextweb.com","213.154.235.236","Z3BNBKV11HV647", "CNAME"],
]


live_values = [
["nutriciavoorjou.nl","dualstack.prd-nvj-sc9-sccd-elb-854392204.eu-west-1.elb.amazonaws.com.","Z3RMNR1WP46MJP", "A"],
["www.nutriciavoorjou.nl","dualstack.prd-nvj-sc9-sccd-elb-854392204.eu-west-1.elb.amazonaws.com.","Z3RMNR1WP46MJP", "A"],
["nutriciababy.be","dualstack.prd-nvj-sc9-sccd-elb-854392204.eu-west-1.elb.amazonaws.com.","Z5QC0VW6FH4AT", "A"],
["www.nutriciababy.be","dualstack.prd-nvj-sc9-sccd-elb-854392204.eu-west-1.elb.amazonaws.com.","Z5QC0VW6FH4AT", "A"],
["hcp-sc9.nutricianextweb.com","dualstack.prd-hcp-sc9-sccd-elb-1511097743.eu-west-1.elb.amazonaws.com.","Z3BNBKV11HV647", "A"],
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
                        'TTL': 60,
                        'ResourceRecords': [
                            {
                                'Value': endpoint
                            },
                        ],
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
                        'TTL': 60,
                        'AliasTarget': {
                            'HostedZoneId': zoneid,
                            'DNSName': endpoint,
                            'EvaluateTargetHealth': False
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
