#Maintainer Bhagvatula Nipun
from modules.ebs import EBS
from modules.ec2 import EC2
from modules.rds import RDS
import time

# def lambda_handler(event, context):
#
#     EC2obj = EC2()
#
#     EBSobj = EBS()
#
#     RDSobj = RDS()
#
#     EC2obj.list()
#     time.sleep(10)
#     EBSobj.list()
#     time.sleep(10)
#     RDSobj.list()
obj = EC2(aws_profile="default",
          aws_default_region="us-east-1")
obj.list()