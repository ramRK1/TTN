import boto3
import json

client = boto3.client('rds')

response = client.describe_db_instances()

db_ids = list()
for db_instance in response['DBInstances']:
    db_ids.append(db_instance['DbiResourceId'])

out="{RDS:"
out=out+[str("{"+i+":"+client.describe_db_instances(Filters=[{'Name': 'db-instance-id','Values': [str(i)]}])+"}") for i in db_ids]
out+="}"
return (out)