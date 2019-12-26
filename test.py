import boto3
tags = [{'Key': 'Created-By', 'Value': 'cost optimizaion task'}, {'Key': 'Cost-Center', 'Value': 'India Auto - Used Car - Classifieds - Classifieds'}, {'Key': 'Name', 'Value': 'Gaadi-store-lms-db-slave1-29-10-19'}]

client = boto3.client('ec2')
response = client.create_tags(Resources=['snap-0d310e3f6cb659719'],Tags=tags)
