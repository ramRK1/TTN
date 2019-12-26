import boto3


class Client:

    def __init__(self, aws_profile=None, aws_default_region=None):
        self.aws_default_region = aws_default_region
        self.aws_profile = aws_profile
        if self.aws_profile is None and self.aws_default_region is None:
            self.session = boto3.Session()
        else:
            self.session = boto3.Session(profile_name=self.aws_profile, region_name=self.aws_default_region)