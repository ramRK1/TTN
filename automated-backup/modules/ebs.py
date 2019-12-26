#Maintainer Bhagvatula Nipun
from .client import Client
import datetime

class EBSInstance:

    def __init__(self, client, info):
        self.client = client
        self.volume_id = info.get('VolumeId')
        self.tags = info.get('Tags')
        self.retention = self.get_retention()
        self.frequency = self.get_frequency()
        self.snapshot_id = self.create_snapshot()
        self.bkpParams = self.backup_params()
        self.retention_checker = self.retention_check()

    def get_frequency(self):
        for tag in self.tags:
            if tag['Key'] == 'Frequency':
                return tag['Value']
            else:
                return 1

    def get_retention(self):
        for tag in self.tags:
            if tag['Key'] == 'Retention':
                return tag['Value']
            else:
                return 7

    def backup_params(self):
        print ('VolumeID: {},Frequency: {},Retention: {}'.format(self.volume_id,self.frequency,self.retention))
        return {'VolumeID': self.volume_id,
                'Frequency': self.frequency, 'Retention': self.retention}

    def create_snapshot(self):
        days = {1: 'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5: 'Friday', 6:'Saturday', 7:'Sunday'}
        now = datetime.datetime.now()
        weekday=now.strftime("%A")

        if days.get(int(self.frequency)) == weekday or  int(self.frequency) == 0:
            today = datetime.datetime.today().strftime('%Y-%m-%d')
            volume_id = self.volume_id
            response = self.client.create_snapshot(
                Description='Automated Snapshot on {}'.format(today),
                VolumeId=volume_id,
                TagSpecifications=[
                    {
                        'ResourceType': 'snapshot',
                        'Tags': [
                            {
                                'Key': 'ManagedBy',
                                'Value': 'ttn-automated-backup'
                            },
                        ]
                    },
                ],
            )
            print ('Creating EBS Snapshot with Id = {}'.format(response['SnapshotId']))
            return response['SnapshotId']

    def retention_check(self):
        datelimit = datetime.datetime.today() - datetime.timedelta(days=int(self.retention))

        pager = self.client.get_paginator('describe_snapshots')
        for page in pager.paginate(Filters=[
            {
                'Name': 'tag:'+'ManagedBy',
                'Values': ['ttn-automated-backup']
            }]):
            for i in page['Snapshots']:
                response = ''
                snapshot_id = i['SnapshotId']
                creationDate = str(i['StartTime']).split(" ")
                ExpectedDate = datetime.datetime.strptime(creationDate[0], "%Y-%m-%d")

                snapshot_tags = self.client.describe_tags(
                    Filters=[
                        {
                            'Name': 'resource-type',
                            'Values':['snapshot']
                        }
                    ])
                for tag in snapshot_tags['Tags']:
                    if tag['Key'] == 'ManagedBy':
                        if ExpectedDate < datelimit:
                            response = self.client.delete_snapshot(
                                SnapshotId=snapshot_id
                            )
                        return response

class EBS(Client, object):

    def __init__(self, aws_profile=None, aws_default_region=None):
        super(EBS, self).__init__(aws_profile=aws_profile,
                                  aws_default_region=aws_default_region)
        self.client = self.session.client('ec2')

    def get_ebs(self):
        ebs = []
        pager = self.client.get_paginator('describe_volumes')
        for page in pager.paginate(Filters=[
            {
                'Name': 'tag:'+'Backup',
                'Values': ['true']
            }]):
            for r in page["Volumes"]:
                    if r['State'] in ['in-use']:
                        ebs.append(EBSInstance(self.client, r))
        return  ebs

    def list(self):
        return self.get_ebs()