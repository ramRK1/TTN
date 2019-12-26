#Maintainer Bhagvatula Nipun
import subprocess
import json
import boto3
import time
import click

class Client:

    def __init__(self, aws_profile=None, aws_default_region=None):
        self.aws_default_region = aws_default_region
        self.aws_profile = aws_profile
        if self.aws_profile is None and self.aws_default_region is None:
            self.session = boto3.Session()
        else:
            self.session = boto3.Session(profile_name=self.aws_profile, region_name=self.aws_default_region)

class CreatFunction(Client, object):

    def __init__(self, aws_profile=None, aws_default_region=None):
        super(CreatFunction, self).__init__(aws_profile=aws_profile,
                                            aws_default_region=aws_default_region)
        self.name = "automated-backup"
        self.iam = self.session.client('iam')
        self.l = self.session.client('lambda')
        self.cloudwatch = self.session.client('events')
        self.policy = self.create_policy( self.name + '-policy')
        self.role = self.create_role(self.name + '-role')
        self.attachpolicy = self.attach_policy()
        time.sleep(5)
        self.lfunc = self.create_function(update=False)
        time.sleep(10)
        self.trigger = self.lambda_schedular()

    def zip_function(self):
        """ creating zip of our lambda function"""
        zipCommand = "zip -r function.zip main.py modules"

        process = subprocess.Popen(zipCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print output

        return output

    def create_policy(self, policyname):
        """Creating the ploicy"""
        policydoc = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "*",
                    "Resource": "*"
                }
            ]
        }
        if policyname in [p['PolicyName'] for p in self.iam.list_policies()['Policies']]:
            print("Policy already exists.")
            policyarn = p['Arn']
        else:

            policyarn = self.iam.create_policy(
                PolicyName=policyname,
                PolicyDocument=json.dumps(policydoc),
                Description='automated backup lambda policy'
            )['Policy']['Arn']

            print ("Automated backup policy created")

        return policyarn

    def create_role(self, name):
        """ Create a role with an optional inline policy """
        asumeroledoc = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": ["lambda.amazonaws.com"]},
                    "Action": ["sts:AssumeRole"]
                },
            ]
        }
        roles = [r['RoleName'] for r in self.iam.list_roles()['Roles']]
        if name in roles:
            print 'IAM role %s exists' % name
            role = self.iam.get_role(RoleName=name)['Role']
        else:
            print 'Creating IAM role %s' % name
            role = self.iam.create_role(RoleName=name,
                                        AssumeRolePolicyDocument=json.dumps(asumeroledoc),
                                        Tags=[{
                                            'Key': 'ManagedBy',
                                            'Value': 'ttn-automated-backup'
                                        }]
                                        )['Role']
        return role

    def attach_policy(self):

        rolename = self.name + '-role'
        policyarn = self.policy

        response = self.iam.attach_role_policy(
            RoleName=rolename,
            PolicyArn=policyarn
        )
        print("Automated backup policy attached")
        return  response

    def create_function(self, update=False):
        """ Create, or update if exists, lambda function """
        do_zip = self.zip_function()
        role = self.role

        with open('function.zip', 'rb') as zipfile:
            if self.name in [f['FunctionName'] for f in self.l.list_functions()['Functions']]:
                if update:
                    print 'Updating %s lambda function code' % self.name
                    return self.l.update_function_code(FunctionName=self.name, ZipFile=zipfile.read())
                else:
                    print 'Lambda function %s exists' % self.name
                    response = self.l.get_function(
                        FunctionName=self.name
                    )['Configuration']['FunctionArn']
                    return  response
            else:
                print 'Creating %s lambda function' % self.name
                for _ in range(3):
                    try:
                        time.sleep(2)
                        response = self.l.create_function(
                            FunctionName=self.name,
                            Runtime='python2.7',
                            Role=role['Arn'],
                            Handler='main.lambda_handler',
                            Description='automated backup lambda',
                            Timeout=120,
                            Publish=True,
                            Code={'ZipFile': zipfile.read()},
                        )['FunctionArn']
                    except InvalidParameterValueException as e:
                        print("Parameter value error: %s" % e)
                    except Exception as e:
                        print(e)
                        continue
                    break
                else:
                    print('Exception when Creating function')
                return response

    def lambda_schedular(self):
        """Creating trigger for lambda"""

        rule_name = self.name + '-trigger'
        if rule_name in [r['Name'] for r in self.cloudwatch.list_rules()['Rules']]:
            print ("Rule already Exists, updating rule and trigger")
        else:
            print("Creating Rule and trigger")

        create_rule = self.cloudwatch.put_rule(
            Name=rule_name,
            ScheduleExpression="rate(24 hours)",
            State='ENABLED',
            Description='Automated backup 24 hr trigger',
            Tags=[
                {
                    'Key': 'ManagedBy',
                    'Value': 'ttn-automated-backup'
                },
            ],
        )
        create_trigger = self.cloudwatch.put_targets(
            Rule='automated-backup-trigger',
            Targets=[
                {
                    'Id': '1',
                    'Arn': self.lfunc,
                }
            ]
        )
        return  create_trigger

@click.command()
@click.option('--profile', default='default', help='Provide aws profile to execute with.')
@click.option('--region', default='us-east-1', help='Provide region to execute in.')
def cli(profile, region):

    obj = CreatFunction(aws_profile=profile,aws_default_region=region)

if __name__ == '__main__':
    cli()