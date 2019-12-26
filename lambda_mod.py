import boto3
import os
import requests

client = boto3.client('lambda')
response = client.list_functions()
c=0
for i in response['Functions']:
    if i['Runtime']=='python2.7':
        func = i['FunctionName']
        response1 = client.get_function(FunctionName=str(func))
        link = response1['Code']['Location']
        r = requests.get(link, allow_redirects=True)
        open('fetch.zip', 'wb').write(r.content)
        os.system('cp ./fetch.zip /home/ram/store/%s.zip'% func)
        os.system('unzip fetch.zip')
        os.system('ls')
        os.system('2to3 -w *.py')
        #os.system('cat lambda_function.py')
        os.system('zip %s.zip *.py'% func)
        os.system('mv ./%s.zip /home/ram/upload/'% func)
        os.system('rm -r *')
        os.system('cd ../upload')
        os.system('ls')
        c+=1
print(c)


# response1 = client.get_function(FunctionName='Bikedekho-one-hour-AMI-deletion')
# link = response1['Code']['Location']
# r = requests.get(link, allow_redirects=True)
# open('fetch.zip', 'wb').write(r.content)
# os.system('unzip fetch.zip')
# os.system('ls -al')
# os.system('2to3 -w lambda_function.py')
# os.system('cat lambda_function.py')
# os.system('mv ./lambda_function.py.bak /home/ram/store/Bikedekho-one-hour-AMI-deletion.py')
