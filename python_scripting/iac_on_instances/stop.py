import boto3

session = boto3.Session(
aws_access_key_id = "AKIA4NYMPNXIOCPIVJXK",
aws_secret_access_key = "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",
    region_name='us-east-1'
)

ec2_client = session.client('ec2')
Instance_id = input('Enter the id of the instance: ')
response = ec2_client.describe_instances(InstanceIds=[Instance_id])
print(response)

if not response['Reservations']:
    print(f"Instance not found")
else:
    ec2_client.stop_instances(InstanceIds=[Instance_id])