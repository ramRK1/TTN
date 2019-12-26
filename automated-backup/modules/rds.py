#Maintainer Bhagvatula Nipun
from .client import Client
import datetime

class RDSInstance:

    def __init__(self, client, info):
        self.client = client
        self.db_id = info.get('DBInstanceIdentifier')
        self.arn = info.get('DBInstanceArn')
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
        print ('RDSInstanceName: {},Frequency: {},Retention: {}'.format(self.db_id,self.frequency,self.retention))
        return {'VolumeID': self.db_id,
                'Frequency': self.frequency, 'Retention': self.retention}

    def create_snapshot(self):
        days = {1: 'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5: 'Friday', 6:'Saturday', 7:'Sunday'}
        now = datetime.datetime.now()
        weekday=now.strftime("%A")

        if days.get(int(self.frequency)) == weekday or  int(self.frequency) == 0:
            today = datetime.datetime.today().strftime('%Y-%m-%d')
            db_id = self.db_id
            response = self.client.create_db_snapshot(
                DBSnapshotIdentifier='{}-Automated-Snapshot-on-{}'.format(db_id,today),
                DBInstanceIdentifier=db_id,
                Tags=[
                            {
                                'Key': 'ManagedBy',
                                'Value': 'ttn-automated-backup'
                            }
                    ])

            print ('Creating RDS Snapshot with name = {}'.format(response['DBSnapshot']['DBSnapshotIdentifier']))
            return response['DBSnapshot']['DBSnapshotIdentifier']

    def retention_check(self):
        datelimit = datetime.datetime.today() - datetime.timedelta(days=int(self.retention))

        pager = self.client.get_paginator('describe_db_snapshots')
        for page in pager.paginate():
            for i in page['DBSnapshots']:
                if i['Status'] in ['available']:
                    response = ''
                    snapshot_arn = i['DBSnapshotArn']
                    snapshot_id = i['DBSnapshotIdentifier']
                    creationDate = str(i['SnapshotCreateTime']).split(" ")
                    ExpectedDate = datetime.datetime.strptime(creationDate[0], "%Y-%m-%d")

                    rds_snapshot_tags = self.client.list_tags_for_resource(ResourceName=snapshot_arn)
                    for tag in rds_snapshot_tags['TagList']:
                            if tag['Key'] == 'ManagedBy':
                                if ExpectedDate < datelimit:
                                    response = self.client.delete_snapshot(SnapshotId=snapshot_id)
                                return response

class RDS(Client, object):

    def __init__(self, aws_profile=None, aws_default_region=None):
        super(RDS, self).__init__(aws_profile=aws_profile,
                                  aws_default_region=aws_default_region)
        self.client = self.session.client('rds')

    def get_rds(self):
        rds = []
        pager = self.client.get_paginator('describe_db_instances')
        for page in pager.paginate():
            for r in page['DBInstances']:
                if r['DBInstanceStatus'] in ['available']:
                    rds_arn = r['DBInstanceArn']
                    rds_tags = self.client.list_tags_for_resource(ResourceName=rds_arn)
                    r['Tags'] = rds_tags['TagList']
                    for tag in rds_tags['TagList']:
                        if tag['Key'] == 'Backup':
                            rds.append(RDSInstance(self.client, r))
        return  rds

    def list(self):
        return self.get_rds()