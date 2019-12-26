import boto3
import datetime
import sys
import pprint
import re


access_key = ""
secret_key = ""
region = "ap-south-1"

ec2 = boto3.client('ec2')


response = ec2.describe_snapshots(
    OwnerIds = ['439876011496']
)['Snapshots']
#response = ec2.describe_snapshots(Filters=[{'Name' : 'owner-alias', 'Values' : ['self']}])['Snapshots']

images = ec2.describe_images(
    Owners = ['439876011496']
)['Images']
#images = ec2.describe_images(Filters=[{'Name' : 'owner-alias', 'Values' : ['self']}])['Images']


image_list = []
for img in images:
    image_list.append(img['ImageId'])
orphan_count = 0
for snapshot in response:
    if snapshot['State'] == 'completed' and re.match(r'[A-Z a-z 0-9]*\(i-[0-9 a-z A-Z]*\)', snapshot['Description']):
        description = snapshot['Description'].split(" ")
        for ami_id in description:
            if "ami-" in ami_id:
                if ami_id in image_list:
                    #print snapshot['Description']
                    print (snapshot['SnapshotId'])
                    print (ami_id)
                    #response = ec2.delete_snapshot(
                    #    SnapshotId=snapshot['SnapshotId']
                    #    )
                    orphan_count+=1

print ("Total Orphan Snapshot Deleted")
print (orphan_count)