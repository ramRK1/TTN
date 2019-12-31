import boto3
import os
import time

client = boto3.client('ec2')
response = client.describe_volumes()
#print(response)

v = []
l = []
for i in response['Volumes']:
    if int(i['Size'])>=500:
        print(i['VolumeId'])
        v.append(str(i['VolumeId']))
        for j in i['Attachments']:
            print(j['InstanceId'])
            l.append(j['InstanceId'])

print(set(l))
print(len(l))
print(len(set(l)))

# sg_l = []
# for ins in l:
#     response = client.describe_instances(InstanceIds=[str(ins)])
#     for i in response['Reservations']:
#         for j in i['Instances']:
#             for sg in j['SecurityGroups']:
#                 sg_l.append(sg['GroupId'])
# print(sg_l)
# print(set(sg_l))

for re in range(len(l)):
    ip = '127.0.0.1'
    OS = ''
    response = client.describe_instances(InstanceIds=[str(l[re])])
    for i in response['Reservations']:
        for j in i['Instances']:
            #print(j)
            try:
                ip = str(j['PublicIpAddress'])
                print(ip)
            except:
                print('No Public IP')
            for ebs in j['BlockDeviceMappings']:
                if str(ebs['Ebs']['VolumeId']) == str(v[re]):
                    print(ebs['DeviceName'])
                    print(v[re])
            #OS = str(j['Platform'])
    print(l[re])
    #print(OS)
    os.system('telnet -E %s 22|grep Ubuntu|wc -l > a.txt'%ip)
    f = open('a.txt','r')
    n = f.read().split('\n')
    print("######################")
    print(n[0])
    if int(n[0]) == 1:
        os.system('ssh -i /home/ram/Downloads/girnar.pem ubuntu@%s \"df -h\"|grep /data'%ip)
        os.system('exit')
    if int(n[0]) == 0:
        os.system('ssh -i /home/ram/Downloads/girnar.pem centos@%s \"df -h\"|grep /data'%ip)
        os.system('exit')
    f.close()
    time.sleep(2)