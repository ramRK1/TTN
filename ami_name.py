import boto3

def ami():
    client = boto3.client('ec2')
    owner_id = boto3.client('sts').get_caller_identity().get('Account')
    filters = [{'Name': 'owner-id', 'Values': [owner_id]}]
    images = boto3.client('ec2').describe_images(Filters=filters)
    for image in images['Images']:
        #print(image)
        #for i in image['Tags'] if i['Name']:
        try:
            if image['Tags']:
                #print(image)
                l=[]
                for tag in image['Tags']:
                    l.append(tag['Key'])
                if 'Name' not in l:
                    response = client.create_tags(Resources=[str(image['ImageId'])],Tags=[{'Key': 'Name','Value': str(image['Name'])}])
                    print(response)
                    print(image['ImageId'])
                    print(image['Name'])
        except:
            response = client.create_tags(Resources=[str(image['ImageId'])],Tags=[{'Key': 'Name','Value': str(image['Name'])}])
            print(response)
            print(image['ImageId'])
            print(image['Name'])

ami()