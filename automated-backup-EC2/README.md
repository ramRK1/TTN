# Config

* For automated-backup to pick your resource and backup parameters, please include these tags with the resources.
  ```
  Backup, Frequency, Retention
  ``` 
* If Backup tag has a value true then the lambda will pick your resource.
* Frequency tag specifies the frequency of backups taken. It has a value from 1-7, representing Monday to Sunday cycle i.e. 1:Monday and 7:Sunday and 0 for everyday backup.
* Retention tag specifies the number of days the backup must be retained before deletion.
 
 Example:

Key   | Value
------------- | -------------
Backup  | true
Frequency | 1
Retention  | 7
  
 The example above means the backup will be taken every Monday (Frequency) and will be Retained for 7 days (Retention).

# Execution Example

Create  zip file of the git repository:

```bash 
zip -r function.zip main.py modules 
 ```
 
Creating Lambda function automated-backup:

```bash
aws lambda create-function --function-name automated-backup --runtime python2.7 --handler main.lambda_handler --zip-file fileb://function.zip --timeout 120 --role <role-arn> --publish
```

Creating event to trigger Lambda daily:

* Creating CloudWatch rule

```bash
aws events put-rule --name automated-backup-trigger --schedule-expression "rate(24 hours)" --role-arn <value> 
```
* Creating CloudWatch target

```bash
aws events put-targets --rule automated-backup-trigger --targets "Id"="1","Arn"="<your-lambda-function-arn>"
```

Role Creation:

```bash
Coming soon
```

Automated deploy script:
* Run the deploy.py to end to end creation of automated backup.

```bash
python deploy.py --profile <you-aws-profile> --region <you-aws-region>
```

* Default values are th e default profile and us-east-1.

# For now it supports

EC2, EBS, RDS