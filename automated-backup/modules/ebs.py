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
        self.backup_date = self.get_date()
        self.snapshot_id = self.create_snapshot()
        self.bkpParams = self.backup_params()
        self.retention_checker = self.retention_check()

    def get_date(self):

        date = ''
        for tag in self.tags:
            if tag['Key'] == 'BackupDate' :
                date = tag['Value']
                break
            else:
                date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
                tag_response = self.client.create_tags(
                    Resources=[str(self.volume_id)],
                    Tags=[
                        {
                            'Key': 'BackupDate',
                            'Value': str(date)
                        },
                    ],
                )
                print(tag_response)
        return date

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
        if int(self.frequency) <= 0:
            print("Please set the frequency value greater than 0")
            return "Please set the frequency value greater than 0"
        else:
            now = datetime.datetime.utcnow()
            create_time = self.backup_date
            today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
            volume_id = self.volume_id
            now = str(now).split()[0]
            built_days = (datetime.datetime.strptime(str(now), "%Y-%m-%d") - datetime.datetime.strptime(str(create_time), "%Y-%m-%d")).days + 1

            if int(built_days) % int(self.frequency) == 0 or int(built_days) == 1:
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
        
        print("Image not created as per the given frequency")
        return "Image not created as per the given frequency"

    def retention_check(self):
        datelimit = datetime.datetime.utcnow() - datetime.timedelta(days=((int(self.retention)-1)*int(self.frequency)))
        print(datelimit)

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