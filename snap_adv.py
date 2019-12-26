import boto3
import json

def snapshots():
    print("Evaluating Snapshots")
    c=0
    f = open("snap_with_ami.csv" , "w+")

    owner_id = boto3.client('sts').get_caller_identity().get('Account')
    filters = [{'Name': 'owner-id', 'Values': [owner_id]}]
    snapshots = boto3.client('ec2').describe_snapshots(Filters=filters)
    for snapshot in snapshots['Snapshots']:
        try:
            if snapshot['Tags']:
                pass
        except:
            if 'Created by' in (snapshot['Description']):
                l=snapshot['Description'].split()
                f.write(str(snapshot['SnapshotId'])+','+str(l[4])+'\n')
                c+=1
            
    print(c)

    f.close()

def ami():
    f = open("snap_with_ami.csv" , "r")
    f1 = open("with_no_tags.csv" , "w+")
    f2 = open("orphans.csv" , "w+")
    l=[[i.split(',')] for i in f.read().split('\n')]
    client = boto3.client('ec2')
    d=0
    e=0
    g=0
    for i in range(len(l)-1):
        try:
            response = client.describe_images(ImageIds=[str(l[i][0][1])])
            for images in response['Images']:
                try:
                    #for tags in images['Tags']:
                    print("Snapshot-id : "+str(l[i][0][0])+','+"AMI-id : "+str(l[i][0][1])+','+"Tags : "+str(images['Tags']))
                    #response = client.create_tags(Resources=[l[i][0][0]],Tags=images['Tags'])
                    #print(l[i][0][0])
                    #print(images['Tags'])
                    d+=1
                except:
                    print("No Tags on AMI with AMI-id "+str(l[i][0][1]))
                    #print(images['Name'])
                    #response = client.create_tags(Resources=[l[i][0][0]],Tags=[{'Key': 'Name','Value': str(images['Name'])}])
                    #f1.write(str(l[i][0][0])+','+str(l[i][0][1])+'\n')
                    e+=1
        except:
            #f2.write(str(l[i][0][0])+'\n')
            #response = client.delete_snapshot(SnapshotId=str(l[i][0][0]))
            g+=1
            print('Corrupted images with AMI-id '+str(l[i][0][1]))
    f.close()
    f1.close()
    f2.close()
    print(d)
    print(e)
    print(g)


snapshots()
ami()