# import json
# import boto3

# def lambda_handler(event, context):
#     # TODO implement
#     s3 = boto3.resource('s3')
#     response = s3.Bucket('ram-ass-bucket')
#     list1=list()
#     for obj in response.objects.all():
#         list1.append((obj.key))
#     return (print(list1))

# import json
# import boto3

# def lambda_handler(event, context):
#     # TODO implement
#     client=boto3.client('ec2')
#     response = client.describe_instances(
#     Filters=[
#         {
#             'Name': 'instance-state-name',
#             'Values': [
#                 'running',
#             ]
#         },
#     ]
#     )
#     return{
#         "body": json.dumps(print(response))
#     }