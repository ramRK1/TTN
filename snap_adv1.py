import boto3
import json

def snapshots():
    print("Evaluating Snapshots")
    c=0
    f = open("orphans.csv" , "w")
    f1 = open("snap_with_ami.csv" , "w")

    owner_id = boto3.client('sts').get_caller_identity().get('Account')
    filters = [{'Name': 'owner-id', 'Values': [owner_id]}]
    snapshots = boto3.client('ec2').describe_snapshots(Filters=filters)
    k = []
    for snapshot in snapshots['Snapshots']:
        try:
            if snapshot['Tags']:
                pass
        except:
            if 'Created by' not in (snapshot['Description']):
                f.write(str(snapshot['SnapshotId'])+','+str(snapshot['Description'])+'\n')
            else:
                desc = snapshot['Description']
                li = desc.split(" ")
                s='\''+li[4]+'\''
                print(s)
                images = boto3.client('ec2').describe_images(ImageIds=[str(li[4])])
                for image in images['Images']:
                    if str(image['Tags']) not in str(image):
                        f1.write(str(snapshot['SnapshotId'])+','+str(li[4])+str({})+'\n')
                    else:
                        f1.write(str(snapshot['SnapshotId'])+','+str(li[4])+','+str(image['Tags'])+'\n')
                
                c+=1
    print(c)

    f.close()
    f1.close()

snapshots()