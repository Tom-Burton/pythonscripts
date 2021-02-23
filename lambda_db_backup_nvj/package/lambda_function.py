import pyodbc
import os
from datetime import date

dbList_sccm = [
    'Nutricia.Analytics.v9',
    'Nutricia.Exm.Master.v9',
    'Nutricia.ExperienceForms.v9',
    'Nutricia.Messaging.v9',
    'Nutricia.Processing.Pools.v9',
    'Nutricia.Processing.Tasks.v9',
    'Nutricia.ReferenceData.v9',
    'Nutricia.Sessions.v9',
    'Nutricia.DataExchange.Verification.v9',
    'Nutricia.MarketingAutomation.v9',
    'Nutricia.Data.v9',
    'Nutricia.Core.v9',
    'Nutricia.Master.v9',
    'Nutricia.Web.v9',
    'Nutricia.Reporting.Primary.v9',
    'Nutricia.Reporting.Secondary.v9',
    'Nutricia.Analytics.v9_Secondary'
]

dbList_sccm3 = [
    'Nutricia.Xdb.Collection.Shard0',
    'Nutricia.Xdb.Collection.Shard1',
    'Nutricia.Xdb.Collection.Shard2',
    'Nutricia.Xdb.Collection.Shard3',
]

dbList_sccm4 = [
    'Nutricia.Xdb.Collection.Shard4',
    'Nutricia.Xdb.Collection.Shard5',
    'Nutricia.Xdb.Collection.Shard6',
    'Nutricia.Xdb.Collection.Shard7',
    'Nutricia.Xdb.Collection.ShardMapManager'
]

def get_env_variable(var_name):
    msg = "Set the %s environment variable"
    try:
        return os.environ[var_name]
    except KeyError:
        var_name = ''
        return var_name

def backupdb(dbName,server):
    today = date.today()
    datestring = today.strftime("%b-%d-%Y")
    sqlPort = 1433
    sqlUsername = 'sitecoreprd'
    sqlPassword = '54BHBefwfBBJrwvT'
    print(pyodbc.drivers())
    print('Attempting Connection...')
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+dbName+';UID='+sqlUsername+';PWD=' +sqlPassword);
    print('Connected!')
    sqlCmd = 'exec msdb.dbo.rds_backup_database @source_db_name=\''+dbName+'\', @s3_arn_to_backup_to=\'arn:aws:s3:::nutricia-rds-backups/'+datestring+'/'+dbName+'\', @overwrite_S3_backup_file=1'
    conn.cursor().execute(sqlCmd)
    print('command executed: '+sqlCmd)
    conn.commit()

def backupchoice():
    env_present_db = get_env_variable('database')
    env_present_server = get_env_variable('server')
    if not env_present_db or env_present_db == 'none':
        for db in dbList_sccm:
            backupdb(db,'prd-nvj-sc9-sccm.c38k0lmfp4fu.eu-west-1.rds.amazonaws.com')
        for db in dbList_sccm3:
            backupdb(db,'prd-nvj-sc9-sccm-3.c38k0lmfp4fu.eu-west-1.rds.amazonaws.com')
        for db in dbList_sccm4:
            backupdb(db,'prd-nvj-sc9-sccm-4.c38k0lmfp4fu.eu-west-1.rds.amazonaws.com')
    else
        backupdb(env_present_db,env_present_server)

if __name__ == "__main__":
    backupchoice()
