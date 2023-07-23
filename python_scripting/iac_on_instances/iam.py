import boto3
import pprint

iam_con_cli = boto3.client(service_name="iam")
pprint.pprint(iam_con_cli.list_users())
response = iam_con_cli.list_users()

for each_user in response:
    print(each_user)

