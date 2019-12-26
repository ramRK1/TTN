import json
import boto3
import os
def ami():
    print('Processing AMI')
    
    owner_id = boto3.client('sts').get_caller_identity().get('Account')
    filters = [{'Name': 'owner-id', 'Values': [owner_id]}]
    images = boto3.client('ec2').describe_images(Filters=filters)

    f = open("output.csv","w")
    f1 = open("corrupt_snaps_ami_id.csv","w")
    count = 0

    for image in images['Images']:
        
        for device in image['BlockDeviceMappings']:
            
            try:
                if device['Ebs']['SnapshotId']:
                    f.write(image['ImageId']+','+image['Name']+','+str(device['Ebs']['SnapshotId'])+'\n')

            except:
                count += 1
                f1.write(image['ImageId']+image['Name']+'\n')
    print('corrupted snaps = '+ str(count))
    return

ami()