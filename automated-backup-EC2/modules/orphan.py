#Maintainer Bhagvatula Nipun && Ram Kamra
from .client import Client
import boto3

class Orphan(Client, object):

    def __init__(self, aws_profile=None, aws_default_region=None):
        super(Orphan, self).__init__(aws_profile=aws_profile,
                                  aws_default_region=aws_default_region)
        self.client = self.session.client('ec2')
    
    def delete_snaps(self, simulate=False):
        id_list = []
        ami_without_snaps = []
        response = self.client.describe_images(Owners=['self'])
        for image in response['Images']:
            try:
                for device in image['BlockDeviceMappings']:
                    id_list.append(device['Ebs']['SnapshotId'])
            except:
                ami_without_snaps.append(image['ImageId'])

        paginator = self.client.get_paginator('describe_snapshots')

        response = paginator.paginate(OwnerIds=['self'])
        
        del_snaps = []
        c = 0
        for page in response:
            for snap in page['Snapshots']:
                snap_id = snap['SnapshotId']
                if snap_id not in id_list:
                    c+=1
                    if simulate == True:
                        del_snaps.append(snap_id)
                    else:
                        res = self.client.delete_snapshot(SnapshotId=str(snap_id))
                        print(res)

        if simulate == True:
            print("These are orphans snapshots total : %s are to be deleted"%(str(c)))
            print(del_snaps)
            print("These are ami's without snapshots total : %s"%(str(len(ami_without_snaps))))
            print(ami_without_snaps)
        else:
            print("Total %s snapshots are deleted"%(str(c)))
            print(del_snaps)
            print("These are ami's without snapshots total : %s"%(str(len(ami_without_snaps))))
            print(ami_without_snaps)
        return del_snaps