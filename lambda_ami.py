import json
import boto3

Tags_Required = ['owner', 'purpose']

def lambda_handler(event, context):
    print('Processing AMI')
    
    owner_id = boto3.client('sts').get_caller_identity().get('Account')
    filters = [{'Name': 'owner-id', 'Values': [owner_id]}]
    images = boto3.client('ec2').describe_images(Filters=filters)
    ami_with_tags = list()
    ami_without_tags = list()
    for image in images['Images']:
        #print(images)
        #print(image)
        if 'Tags' in image:
            tags = image['Tags']
        else:
            tags = []
        #print(tags)
        tags_list = list()
        for tag in tags:
            tags_list.append(tag['Key'])
            #print(tags_list)
        Tags_Required.sort()
        tags_list.sort()
        if set(tags_list) <= set(Tags_Required):
            ami_with_tags.append(image['ImageId'])
        else:
            ami_without_tags.append(image['ImageId'])
        #print(ami_with_tags)
        #print(ami_without_tags)
    return { "ami_ids_with_tags": ami_with_tags, "ami_ids_without_tags": ami_without_tags }