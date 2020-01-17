#Maintainer Bhagvatula Nipun && Ram Kamra
from .client import Client
import datetime
import copy
import boto3

class EC2Instance:

    def __init__(self, client, info, simulate, simulate_createami, simulate_deami, simulate_snapdelete):
        self.client = client
        self.instance_id = info.get('InstanceId')
        self.tags = info.get('Tags')
        if simulate == False:
            print("--------------------------------------------------------------")
            print(self.tags)
        self.retention = self.get_retention()
        self.frequency = self.get_frequency()
        self.backup_date = self.get_date(simulate)
        self.sync = self.snapshot_delete(simulate, simulate_snapdelete)
        self.ami_id = self.create_ami(simulate,simulate_createami)
        self.bkpParams = self.backup_params(simulate)
        self.retention_checker = self.retention_check(simulate,simulate_deami)
        self.create_datetag = self.create_date(simulate)

    def create_date(self, simulate):
        if simulate == False:
            tag_response = self.client.create_tags(
                Resources=[str(self.instance_id)],
                Tags=[
                    {
                        'Key': 'BackupDate',
                        'Value': str(self.backup_date)
                    },
                ],
            )
        return "Created Backup Date Tag"

    def get_date(self, simulate):

        date = ''
        for tag in self.tags:
            if tag['Key'] == 'BackupDate' :
                date = tag['Value']
                break
            if tag['Key'] == 'backupdate' :
                date = tag['Value']
                break
            else:
                date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
        return date
    
    def get_frequency(self):

        freq = ''
        for tag in self.tags:
            if tag['Key'] == 'rotate' :
                freq = tag['Value']
                break
            else:
                freq = 1
        return freq

    def get_retention(self):

        ret = ''
        for tag in self.tags:
            if tag['Key'] == 'retention':
                ret =  tag['Value']
                break
            else:
                ret = 7
        return  ret

    def backup_params(self, simulate):
        if simulate == False:
            print('InstanceID: {}, Frequency: {}, Retention: {}'.format(self.instance_id,self.frequency,self.retention))
        return {'InstanceID': self.instance_id,
                'Frequency': self.frequency, 'Retention': self.retention}

    def snapshot_delete(self, simulate, simulate_snapdelete):
        snapshots = []
        for response in self.client.get_paginator('describe_snapshots').paginate(Filters=[{'Name': 'tag:automated-backup-delta','Values': ['true']}],OwnerIds=['self']):
            snapshots = [snapshot['SnapshotId'] for snapshot in response['Snapshots']]
        if simulate == True:
            if len(snapshots) > 0:
                simulate_snapdelete.append(snapshots)
        else:
            if len(snapshots) > 0:
                for snap_id in snapshots:
                    self.client.delete_snapshot(SnapshotId=str(snap_id))
        return "Snapshots checked and deleted"

    def create_ami(self,simulate,simulate_createami):
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
                if simulate == True:
                    simulate_createami.append(instance_id)
                    return
                else:
                    try:
                        response = self.client.create_image(
                            InstanceId=instance_id,
                            Name='Backup_{}_on_{}'.format(instance_id, today),
                            NoReboot=True
                        )
                        tag_response = self.client.create_tags(
                            Resources=[
                                str(response['ImageId']),
                            ],
                            Tags=[
                                {
                                    'Key': 'ManagedBy',
                                    'Value': 'automated-backup'
                                },
                            ],
                        )
        
                        print ('Creating EC2 AMI with Id = {}'.format(response['ImageId']))
                    except:
                        pass
                    return "Images Formed"
        
        return "Image will not be created as per the frequency for today"

    def retention_check(self,simulate,simulate_deami):
        ami_response_total = self.client.describe_images(
            Filters=[
                {
                    'Name': 'tag:'+'ManagedBy',
                    'Values': ['automated-backup']
                },
            ],
            Owners=['self']
        )
        ami_response = []
        instid = str(self.instance_id)
        for i in ami_response_total['Images']:
            if instid in i['Name'].split('_'):
                ami_response.append(i)

        print(ami_response)
        if len(ami_response) <= int(self.retention):
            return

        datelimit = datetime.datetime.utcnow() - datetime.timedelta(days=((int(self.retention))*int(self.frequency)))
        if simulate == False:
            print(datelimit)

        for i in ami_response:
            creationDate = i['Name'].split("_")[3]
            ami_id = i['ImageId']
            ExpectedDate = datetime.datetime.strptime(creationDate, "%Y-%m-%d")

            if ExpectedDate < datelimit:
                if simulate == True:
                    simulate_deami.append(ami_id)
                else:
                    self.client.deregister_image(ImageId=ami_id)
                    try:
                        for device in i['BlockDeviceMappings']:
                            
                            snap_id = device['Ebs']['SnapshotId']

                            self.client.create_tags(
                                Resources=[str(snap_id)],
                                Tags=[
                                    {
                                        'Key': 'automated-backup-delta',
                                        'Value': 'true'
                                    },
                                ],
                            )
                    except:
                        pass
        return "Retention is checked as per the values the work is done"

class EC2(Client, object):

    def __init__(self, aws_profile=None, aws_default_region=None):
        super(EC2, self).__init__(aws_profile=aws_profile,
                                  aws_default_region=aws_default_region)
        self.client = self.session.client('ec2')

    def get_instance(self, simulate, simulate_createami, simulate_deami, simulate_snapdelete):
        ec2s = []
        instances_list = []
        pager = self.client.get_paginator('describe_instances')
        filters = [{
                        'Name': 'tag:'+'backup',
                        'Values': ['true']
                    }
                ]
        for page in pager.paginate(Filters=filters):
            instances_list.append(page)
        
        # filters = [{
        #                 'Name': 'tag:'+'Backup',
        #                 'Values': ['true']
        #             }
        #         ]
        # for page in pager.paginate(Filters=filters):
        #     instances_list.append(page)

        c=0
        for page in instances_list:
            for r in (page["Reservations"]):
                for i in r['Instances']:
                    if i['State']['Name']:
                        if i['State']['Name'] not in ['terminated']:
                            c+=1
                            ec2s.append(EC2Instance(self.client, i, simulate, simulate_createami, simulate_deami, simulate_snapdelete))

        if simulate == True:
            if len(simulate_createami) == 0:
                print("No AMI's will be created from total instances : %s"%(str(c)))
            else:
                print("AMI of following instances will be created count as %s from total instances : %s"%(str(len(simulate_createami)),str(c)))
                print(simulate_createami)
            if len(simulate_snapdelete) == 0:
                print("No snapshot will be deleted")
            else:
                print("These snapshots with following SnapshotIds will be deleted")
                print(simulate_snapdelete)
            if len(simulate_deami) == 0:
                print("No AMI's will be deregistered")
            else:
                print("AMI with following AMI ID will be deregistered count as %s"%(str(len(simulate_deami))))
                print(simulate_deami)

        return  ec2s

    def listing(self,simulate=False):
        simulate_createami = []
        simulate_deami = []
        simulate_snapdelete = []
        return self.get_instance(simulate, simulate_createami, simulate_deami, simulate_snapdelete)