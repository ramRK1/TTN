import boto3

client = boto3.client('ec2')
l=[]
m=[]
paginator = client.get_paginator('describe_instances')
response_iterator = paginator.paginate()
for j in response_iterator:
    #print(j)
    for i in j['Reservations']:
        for inst in i['Instances']:
            try:
                if inst['InstanceLifecycle'] == 'spot' or inst['InstanceLifecycle'] == 'scheduled':
                    pass
            except:
                l.append(inst['InstanceId'])
                m.append(inst['InstanceType'])


print(l)

file = open('on-demand_inst.csv','w')
for i in range(len(l)):
    file.write(str(l[i])+','+str(m[i])+'\n')
file.close()