import boto3
import os
import requests

client = boto3.client('lambda')
response = client.list_functions()
c=0
for i in response['Functions']:
    if i['Runtime']=='python2.7':
        func = i['FunctionName']
        print(func)
        #func = 'lambdatest'
        response2 = client.update_function_configuration(FunctionName=str(func), Runtime='python3.6')
        print(response2)
        response1 = client.get_function(FunctionName=str(func))
        print(response1)
        link = response1['Code']['Location']
        print(link)
        r = requests.get(link, allow_redirects=True)
        open('fetch.zip', 'wb').write(r.content)
        print('hello1')
        os.system('unzip fetch.zip')
        os.system('mv ./fetch.zip /home/ram/store/%s.zip'% func)
        os.system('ls -al')
        os.system('2to3 -w *.py')
        print('hello2')
        #os.system('cat lambda_function.py')
        os.system('zip %s.zip *.py'% func)
        os.system('mv ./%s.zip /home/ram/upload/'% func)
        os.system('rm -r *')
        # os.system('cd ../upload')
        # os.system('ls -al')
        s='/home/ram/upload/'+str(func)+'.zip'
        print(s)
        os.system('aws lambda update-function-code --function-name %s --zip-file=fileb://%s' % (func,s))
        # response3 = client.update_function_code(FunctionName=str(func), ZipFile=str(s))
        # print(response3)
        c+=1
print(c)