#Maintainer Bhagvatula Nipun && Ram Kamra
from .client import Client
import datetime
import copy
import boto3

class EC2Instance:

    def __init__(self, client, info):
        self.client = client
        self.instance_id = info.get('InstanceId')
        self.tags = info.get('Tags')
        print(self.tags)
        print("----------------------")
        self.retention = self.get_retention()
        self.frequency = self.get_frequency()
        self.backup_date = self.get_date()
        #try:
        self.ami_id = self.create_ami()
        #except:
        #    print("Resource already exists !!!!")
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
                    Resources=[str(self.instance_id)],
                    Tags=[
                        {
                            'Key': 'BackupDate',
                            'Value': str(date)
                        },
                    ],
                )
        return date
    
    def get_frequency(self):

        freq = ''
        for tag in self.tags:
            if tag['Key'] == 'Frequency' :
                freq = tag['Value']
                break
            else:
                freq = 1
        return freq

    def get_retention(self):

        ret = ''
        for tag in self.tags:
            if tag['Key'] == 'Retention':
                ret =  tag['Value']
                break
            else:
                ret = 7
        return  ret

    def backup_params(self):
        print('InstanceID: {}, Frequency: {}, Retention: {}'.format(self.instance_id,self.frequency,self.retention))
        return {'InstanceID': self.instance_id,
                'Frequency': self.frequency, 'Retention': self.retention}

    def boto3_tag_list_to_ansible_dict(self, tags_list):

        tags_dict = {}
        for tag in tags_list:
            if 'key' in tag and not tag['key'].startswith('aws:'):
                tags_dict[tag['key']] = tag['value']
            elif 'Key' in tag and not tag['Key'].startswith('aws:'):
                tags_dict[tag['Key']] = tag['Value']
        return tags_dict

    def ansible_dict_to_boto3_tag_list(self, tags_dict):

        tags_list = []
        for k, v in tags_dict.items():
            tags_list.append({'Key': k, 'Value': v})
        return tags_list

    def snapshot_tag(self, imageId):

        snapshots = {}

        for response in self.client.get_paginator('describe_snapshots').paginate(OwnerIds=['self']):
            snapshots.update([(snapshot['SnapshotId'], snapshot) for snapshot in response['Snapshots']])

        for image in self.client.describe_images(Owners=['self'],ImageIds=[imageId])['Images']:
            tags = self.boto3_tag_list_to_ansible_dict(image.get('Tags', []))
            # to tag volumes, e.g., (1/3) (2/3) (3/3)
            devnum = 0
            numberofdevs=len(image['BlockDeviceMappings'])
            for device in image['BlockDeviceMappings']:
                if 'SnapshotId' in device['Ebs']:
                    snapshot_id = {}
                    devnum += 1
                    snapshot_id = snapshots[device['Ebs']['SnapshotId']]
                    snapshot_id['Used'] = True
                    print(snapshot_id)
                    cur_tags = self.boto3_tag_list_to_ansible_dict(snapshot_id.get('Tags', []))
                    new_tags = copy.deepcopy(cur_tags)
                    new_tags.update(tags)
                    new_tags['ImageId'] = image['ImageId']
                    # here's where to change formatting
                    new_tags['Name'] = 'AMI:' + image['Name'] + ' ' + device['DeviceName'] + ' (' + str(devnum) + '/' + str(numberofdevs) + ')'
                    if new_tags != cur_tags:
                        print('{}: Tags changed to {}'.format(snapshot_id['SnapshotId'], new_tags))
                        self.client.create_tags(Resources=[snapshot_id['SnapshotId']], Tags=self.ansible_dict_to_boto3_tag_list(new_tags))

    def create_ami(self):
        if int(self.frequency) <= 0:
            print("Please set the frequency value greater than 0")
        else:
            now = datetime.datetime.utcnow()
            create_time = self.backup_date
            today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
            instance_id = self.instance_id

            now = str(now).split()[0]
            built_days = (datetime.datetime.strptime(str(now), "%Y-%m-%d") - datetime.datetime.strptime(str(create_time), "%Y-%m-%d")).days + 1

            if int(built_days) % int(self.frequency) == 0 or int(built_days) == 1:
                response = self.client.create_image(
                    InstanceId=instance_id,
                    Name='Automated Backup {} on {}'.format(instance_id, today),
                    NoReboot=True
                )

                tag_response = self.client.create_tags(
                    Resources=[
                        str(response['ImageId']),
                    ],
                    Tags=[
                        {
                            'Key': 'ManagedBy',
                            'Value': 'ttn-automated-backup'
                        },
                    ],
                )

                print(tag_response)
                print ('Creating EC2 AMI with Id = {}'.format(response['ImageId']))
                self.snapshot_tag(response['ImageId'])
                return response['ImageId']

        print("Image not created as per the given frequency")
        return "Image not created as per the given frequency"

    def retention_check(self):
        datelimit = datetime.datetime.utcnow() - datetime.timedelta(days=((int(self.retention)-1)*int(self.frequency)))
        print(datelimit)

        ami_response = self.client.describe_images(
            Filters=[
                {
                    'Name': 'tag:'+'ManagedBy',
                    'Values': ['ttn-automated-backup']
                }
            ])
        print(ami_response)
        for i in ami_response['Images']:
            response = ''
            creationDate = i['CreationDate'].split("T")
            ami_id = i['ImageId']
            ExpectedDate = datetime.datetime.strptime(creationDate[0], "%Y-%m-%d")

            tag_response = self.client.describe_tags(
                Filters=[
                    {
                        'Name': 'resource-id',
                        'Values': [ami_id]
                    }
                ])

            for tag in tag_response['Tags']:
                if tag['Key'] == 'ManagedBy':
                    if ExpectedDate < datelimit:
                        self.client.deregister_image(ImageId=ami_id)

            for device in i['BlockDeviceMappings']:
                print(device)
                snap_id = device['Ebs']['SnapshotId']

                print(snap_id)

                snap_tag_response = self.client.describe_snapshots(SnapshotIds=[snap_id])

                print(snap_tag_response)

                for snaps in snap_tag_response['Snapshots']:
                    try:
                        for tag in snaps['Tags']:
                            if tag['Key'] == 'ManagedBy':
                                if ExpectedDate < datelimit:
                                    self.client.delete_snapshot(SnapshotId=snap_id)
                    except:
                        pass

        return

class EC2(Client, object):

    def __init__(self, aws_profile=None, aws_default_region=None):
        super(EC2, self).__init__(aws_profile=aws_profile,
                                  aws_default_region=aws_default_region)
        self.client = self.session.client('ec2')

    def get_instance(self):
        ec2s = []
        pager = self.client.get_paginator('describe_instances')
        for page in pager.paginate(Filters=[
            {
                'Name': 'tag:'+'Backup',
                'Values': ['true']
            }]):
                for r in (page["Reservations"]):
                    for i in r['Instances']:
                        if i['State']['Name']:
                            if i['State']['Name'] not in ['terminated']:
                                ec2s.append(EC2Instance(self.client, i))

        return  ec2s

    def list(self):
        return self.get_instance()