import boto3

client = boto3.client('ce')
# response = client.get_dimension_values(
#     TimePeriod={
#         'Start': '2019-12-01',
#         'End': '2019-12-30'
#     },
#     Dimension='PURCHASE_TYPE',
#     Context='COST_AND_USAGE',
# )

response = client.get_cost_and_usage(
    TimePeriod={
        'Start': '2019-12-01',
        'End': '2019-12-30'
    },
    Granularity='MONTHLY',
    Filter={
        # 'Or': [
        #     {'... recursive ...'},
        # ],
        # 'And': [
        #     {'... recursive ...'},
        # ],
        # 'Not': {'... recursive ...'},
        'Dimensions': {
            'Key': 'PURCHASE_TYPE',
            'Values': [
                'On Demand Instances',
            ]
        },
        # 'Tags': {
        #     'Key': 'string',
        #     'Values': [
        #         'string',
        #     ]
        # },
        # 'CostCategories': {
        #     'Key': 'string',
        #     'Values': [
        #         'string',
        #     ]
        # }
    },
    Metrics=[
        'UnblendedCost',
    ],
    # GroupBy=[
    #     {
    #         'Type': 'DIMENSION'|'TAG'|'COST_CATEGORY',
    #         'Key': 'string'
    #     },
    # ],
    # NextPageToken='string'
)


print(response)