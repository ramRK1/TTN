import datetime
import json
with open('/home/ram/Downloads/new_image.json', 'r') as f:
    text = json.load(f)

ret = input("Enter the number of days to check for retention policy\n")
datelimit = datetime.datetime.today() - datetime.timedelta(days=int(ret))

valid_resource_count = 0
nonvalid_resource_count = 0
for t in text:
    creationDate = t['creationTimestamp']
    ExpectedDate = datetime.datetime.strptime(creationDate.split("T")[0], "%Y-%m-%d")
    if ExpectedDate > datelimit:
        valid_resource_count += 1
    else:
        nonvalid_resource_count += 1

print("valid resources = %d" %valid_resource_count)
print("unvalid resources = %d" %nonvalid_resource_count)