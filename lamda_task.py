import json
import boto3

tags_required = ['owner', 'purpose']

def lambda_handler(event, context):
    print('Processing AMI')
    
    owner_id = boto3.client('sts').get_caller_identity().get('Account')
    filters = [{'Name': 'owner-id', 'Values': [owner_id]}]
    images = boto3.client('ec2').describe_images(Filters=filters)
    snapshots = boto3.client('ec2').describe_snapshots(Filters=filters)
    tags_required.sort()
    
    ami_with_tags = list()
    ami_without_tags = list()
    for image in images['Images']:
#        print(images)
#        print(image)
        if 'Tags' in image:
            tags = image['Tags']
        else:
            tags = []
#        print(tags)
        tags_list = list()
        for tag in tags:
            tags_list.append(tag['Key'])
#            print(tags_list)
        tags_list.sort()
        if set(tags_list) <= set(tags_required):
            ami_with_tags.append(image['ImageId'])
        else:
            ami_without_tags.append(image['ImageId'])
#        print(ami_with_tags)
#        print(ami_without_tags)
    
    print("Processing Snapshots")
    
    snap_with_tags = list()
    snap_without_tags = list()
    for snapshot in snapshots['Snapshots']:
#        print(snapshots)
#        print(snapshot)
        if 'Tags' in snapshot:
            tags = snapshot['Tags']
        else:
            tags = []
#        print(tags)
        tags_list = list()
        for tag in tags:
            tags_list.append(tag['Key'])
#            print(tags_list)
        tags_list.sort()
        if set(tags_list) <= set(tags_required):
            snap_with_tags.append(snapshot['SnapshotId'])
        else:
            snap_without_tags.append(snapshot['SnapshotId'])
#        print(snap_with_tags)
#        print(snap_without_tags)
        
    return ({"ami_ids_with_tags":ami_with_tags}, {"ami_ids_without_tags":ami_without_tags}, {"snap_ids_with_tags":snap_with_tags}, {"snap_ids_without_tags":snap_without_tags})