import boto3
import json

def snapshots():
    print("Evaluating Snapshots")
    c=0
    snap_ids = list()
    snap_tags = list()
    f = open("snap.csv","w")

    owner_id = boto3.client('sts').get_caller_identity().get('Account')
    filters = [{'Name': 'owner-id', 'Values': [owner_id]}]
    snapshots = boto3.client('ec2').describe_snapshots(Filters=filters)
    for snapshot in snapshots['Snapshots']:
        #print(snapshot)
        if str(snapshot['Description'])=='Created for policy: policy-01a8dc510a66a9867 schedule: Daily-Backup':
            pass
        elif str(snapshot['Description'])=='Created for policy: policy-09dcf7dd4bf3d2407 schedule: Volume_Daily_Backup':
            pass
        elif str(snapshot['Description'])=='This snapshot is created by the AWS Backup service.':
            pass
        else:
            snap_ids.append(snapshot['SnapshotId'])
            try:
                for tags in snapshot['Tags']:
                    snap_tags.append(tags)
            except:
                snap_tags.append({})
            c+=1
    
    for i in range(c):
        f.write(str(snap_ids[i])+","+str(snap_tags[i])+"\n")

    print(c)

snapshots()