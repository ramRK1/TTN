import boto3
from datetime import datetime
client = boto3.client('cloudwatch')

total_nov = 0
total_dec = 0
total_jan = 0
request_nov = 0
request_dec = 0
request_jan = 0

response = client.get_metric_data(
    MetricDataQueries=[
        {
            'Id': 'totalcount',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/ApplicationELB',
                    'MetricName': 'HTTPCode_ELB_5XX_Count',
                    'Dimensions': [
                        {
                            'Name': 'LoadBalancer',
                            'Value': 'app/zigwheels-prod/20671b7435ccafed'
                        },
                    ]
                },
                'Period': 2592000,
                'Stat': 'Sum',
                'Unit': 'Count'
            },
            'Label': 'zigwheels-prod 5xx count',
        },
    ],
    StartTime=datetime(2019, 11, 1),
    EndTime=datetime(2019, 11, 30)
)

response2 = client.get_metric_data(
    MetricDataQueries=[
        {
            'Id': 'particularcount2',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/ApplicationELB',
                    'MetricName': 'HTTPCode_ELB_5XX_Count',
                    'Dimensions': [
                        {
                            'Name': 'LoadBalancer',
                            'Value': 'app/zigwheels-prod/20671b7435ccafed'
                        },
                    ]
                },
                'Period': 2678400,
                'Stat': 'Sum',
                'Unit': 'Count'
            },
            'Label': 'zigwheels-prod 5xx count',
        },
    ],
    StartTime=datetime(2019, 12, 1),
    EndTime=datetime(2019, 12, 31)
)

response3 = client.get_metric_data(
    MetricDataQueries=[
        {
            'Id': 'particularcount3',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/ApplicationELB',
                    'MetricName': 'HTTPCode_ELB_5XX_Count',
                    'Dimensions': [
                        {
                            'Name': 'LoadBalancer',
                            'Value': 'app/zigwheels-prod/20671b7435ccafed'
                        },
                    ]
                },
                'Period': 1209600,
                'Stat': 'Sum',
                'Unit': 'Count'
            },
            'Label': 'zigwheels-prod 5xx count',
        },
    ],
    StartTime=datetime(2020, 1, 1),
    EndTime=datetime(2020, 1, 14)
)

response1 = client.get_metric_data(
    MetricDataQueries=[
        {
            'Id': 'particularcount1',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/ApplicationELB',
                    'MetricName': 'RequestCount',
                    'Dimensions': [
                        {
                            'Name': 'LoadBalancer',
                            'Value': 'app/zigwheels-prod/20671b7435ccafed'
                        },
                    ]
                },
                'Period': 2592000,
                'Stat': 'Sum',
                'Unit': 'Count'
            },
            'Label': 'zigwheels-prod RequestCount',
        },
    ],
    StartTime=datetime(2019, 11, 1),
    EndTime=datetime(2019, 11, 30)
)

response4 = client.get_metric_data(
    MetricDataQueries=[
        {
            'Id': 'total2',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/ApplicationELB',
                    'MetricName': 'RequestCount',
                    'Dimensions': [
                        {
                            'Name': 'LoadBalancer',
                            'Value': 'app/zigwheels-prod/20671b7435ccafed'
                        },
                    ]
                },
                'Period': 2678400,
                'Stat': 'Sum',
                'Unit': 'Count'
            },
            'Label': 'zigwheels-prod RequestCount',
        },
    ],
    StartTime=datetime(2019, 12, 1),
    EndTime=datetime(2019, 12, 31)
)

response5 = client.get_metric_data(
    MetricDataQueries=[
        {
            'Id': 'total3',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/ApplicationELB',
                    'MetricName': 'RequestCount',
                    'Dimensions': [
                        {
                            'Name': 'LoadBalancer',
                            'Value': 'app/zigwheels-prod/20671b7435ccafed'
                        },
                    ]
                },
                'Period': 1209600,
                'Stat': 'Sum',
                'Unit': 'Count'
            },
            'Label': 'zigwheels-prod RequestCount',
        },
    ],
    StartTime=datetime(2020, 1, 1),
    EndTime=datetime(2020, 1, 14)
)

for i in response1['MetricDataResults']:
    total_nov = i['Values'][0]

for i in response1['MetricDataResults']:
    total_dec = i['Values'][0]

for i in response1['MetricDataResults']:
    total_jan = i['Values'][0]

for i in response2['MetricDataResults']:
    request_dec = i['Values'][0]

for i in response3['MetricDataResults']:
    request_jan = i['Values'][0]

for i in response['MetricDataResults']:
    request_nov = i['Values'][0]

print(100-((request_nov/total_nov)*100))
print(100-((request_dec/total_dec)*100))
print(100-((request_jan/total_jan)*100))