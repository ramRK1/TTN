#Maintainer Bhagvatula Nipun && Ram kamra
from modules.ec2 import EC2
from modules.orphan import Orphan

import time

def lambda_handler(event, context):
    EC2obj = EC2()
    EC2obj.listing(simulate=True)

    Orphanobj = Orphan()
    Orphanobj.delete_snaps(simulate=True)