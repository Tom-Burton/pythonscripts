#! /usr/bin/python

import boto3
import datetime
import sys
import time

db_names = sys.argv
db_names.pop(0)
region = 'eu-west-1'
account_id = '607572287073'
retention_days = 15
loop_wait = 20
backups_dict = {} #dict of backup job id:job status
start_time = time.time()


def main():
    print("Connecting to AWS Backup Service")
    session = boto3.Session(profile_name='nutricia-terraform')
    client = session.client('backup', region_name=region)
    readable_date = datetime.datetime.now().strftime("%Y-%b-%a-%H-%M")
    for db in db_names:
        backups_dict[create_backup(db, client)] = 'started'
    print('Pulling backup job status from AWS Backup Service')
    while True:
        for key in backups_dict:
            backup_response = get_backup_status(key, client)
            backup_status = backup_response['State']
            backups_dict[key] = backup_status
            resource = backup_response['ResourceArn']
            print(f'Backup Status: {resource} = {backup_status}')
            completion = 'COMPLETED'
            for key in backups_dict:
                if backups_dict[key] != 'COMPLETED':
                    completion = backups_dict[key]
                    print(f'waiting on job {key}.')
        if len(backups_dict) == len(db_names) and completion == 'COMPLETED':
            print('All jobs complete!')
            duration = round(time.time() - start_time, 2)
            print(f'Completion time: {duration}')
            break
        print(f' Next update in {loop_wait} seconds')
        time.sleep(loop_wait)

def create_backup(db, client):
    token = f'{db}-{datetime.datetime.now().strftime("%Y-%b-%a-%H-%M")}'
    response = client.start_backup_job(
        BackupVaultName='Default',
        ResourceArn=f'arn:aws:rds:{region}:{account_id}:db:{db}',
        IamRoleArn=f'arn:aws:iam::{account_id}:role/service-role/AWSBackupDefaultServiceRole',
        IdempotencyToken=f'{token}',
        Lifecycle={
            'DeleteAfterDays': retention_days
        }
    )
    backup_id = response['BackupJobId']
    print(f'RDS backup started: {db}  ---  id: {backup_id}')
    return backup_id


def get_backup_status(backup_id, client):
    response = client.describe_backup_job(
        BackupJobId = f'{backup_id}'
    )
    status = response['State']
    return response


if __name__ == "__main__":
    main()
