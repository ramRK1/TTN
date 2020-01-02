import boto3
import sys
from datetime import datetime, timedelta

client = boto3.client('ec2')
client1 = boto3.client('cloudwatch')
# l=[]
# m=[]
a = {}
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
                Name = ''
                for tag in inst['Tags']:
                    if tag['Key'] == "Name":
                        Name = tag['Value']
                        break
                    else:
                        Name = ''
                a.update({inst['InstanceId']: [inst['InstanceType'],Name]})
                # l.append(inst['InstanceId'])
                # m.append(inst['InstanceType'])

a = {k: v for k, v in sorted(a.items(), key=lambda item: item[1][0])}
print(type(a))
print(a)
file = open('on-demand_inst.csv','w')
for i in a:
    avg_12hr = ''
    avg_3days = ''
    avg_7days = ''
    response = client1.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {
            'Name': 'InstanceId',
            'Value': str(i)
            },
        ],
        StartTime=(datetime.now() - timedelta(hours=12)).isoformat(),
        EndTime=datetime.now().isoformat(),
        Period=43200,
        Statistics=[
            'Average',
        ],
        Unit='Percent'
    )
    for j in response['Datapoints']:
        avg_12hr = j['Average']
    
    response2 = client1.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {
            'Name': 'InstanceId',
            'Value': str(i)
            },
        ],
        StartTime=(datetime.now() - timedelta(days=3)).isoformat(),
        EndTime=datetime.now().isoformat(),
        Period=259200,
        Statistics=[
            'Average',
        ],
        Unit='Percent'
    )
    for j in response2['Datapoints']:
        avg_3days = j['Average']

    response3 = client1.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {
            'Name': 'InstanceId',
            'Value': str(i)
            },
        ],
        StartTime=(datetime.now() - timedelta(days=7)).isoformat(),
        EndTime=datetime.now().isoformat(),
        Period=604800,
        Statistics=[
            'Average',
        ],
        Unit='Percent'
    )
    for j in response3['Datapoints']:
        avg_7days = j['Average']
    
    # response = client.describe_instances(InstanceIds=[str(i)])
    # for j in response['Reservations']:
    #     for inst in j['Instances']:
    #         for tag in inst['Tags']:
    #             if tag['key'] == "Name":
    #                 Name = tag['Value']
    #                 break
    #             else:
    #                 Name = ''

    file.write(str(a[i][1])+","+str(i)+","+str(a[i][0])+","+"normal,"+str(avg_12hr)+","+str(avg_3days)+","+str(avg_7days)+"\n")
file.close()



# with open('on-demand_inst.csv','r') as file:
#     for line in file:
#         print(line)
#         ins_id,ins_type = line.split(",")
#         response = client1.get_metric_statistics(
#             Namespace='AWS/EC2',
#             MetricName='CPUUtilization',
#             Dimensions=[
#                 {
#                 'Name': 'InstanceId',
#                 'Value': str(ins_id)
#                 },
#             ],
#             StartTime=(datetime.now() - timedelta(hours=12)).isoformat(),
#             EndTime=datetime.now().isoformat(),
#             Period=43200,
#             Statistics=[
#                 'Average',
#             ],
#             Unit='Percent'
#         )
#         print(response)

# for cpu in response:
#     if cpu['Key'] == 'Average':
#         k = cpu['Value']
# print(k)

# file = open('on-demand_inst.csv','w')
# for i in range(len(l)):
#     file.write(str(l[i])+','+str(m[i])+'\n')
# file.close()