import boto3

def ec2_snapshots():
    ec2_snap = []
    paginator = client.get_paginator('describe_snapshots')
    try:
        for page in paginator.paginate(RestorableByUserIds=['all'],OwnerIds=[str(owner_id)]):
            print(page)
            for image in page['Snapshots']:
                ec2_snap.append(image['SnapshotId'])
        return ec2_snap
    except:
        return []

def ec2_ami():
    ec2_ami = []
    response = client.describe_images(
        ExecutableUsers=['all'],
        Filters=[
            {
                'Name': 'is-public',
                'Values': ['true']
            },
        ],
        Owners=[str(owner_id)],
    )
    print(response)

    for image in response['Images']:
        ec2_ami.append(image['ImageId'])
    return ec2_ami

def rds_snapshots():
    rds_snap = []
    client = boto3.client('rds')
    paginator = client.get_paginator('describe_db_instances')
    try:
        for page in paginator.paginate(SnapshotType='public'):
            print(page)
            for image in page['DBSnapshots']:
                rds_snap.append(image['DBSnapshotArn'])
        return rds_snap
    except:
        return []


owner_id = boto3.client('sts').get_caller_identity().get('Account')
client = boto3.client('ec2')
public_ec2_ami = ec2_ami()
public_ec2_snapshots = ec2_snapshots()
public_rds_snapshots = rds_snapshots()

print(public_ec2_ami)
print(public_ec2_snapshots)
print(public_rds_snapshots)