import boto3

session= boto3.Session(
aws_access_key_id = "AKIA4NYMPNXIOCPIVJXK",
aws_secret_access_key = "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",
    region_name='us-east-1'
)

ec2_client= session.client('ec2')
instance_id = input("enter you instance to start:")
response = ec2_client.describe_instances(InstanceIds=[instance_id])
print(response)

if not response['Reservations']:
    print("Instance not found")
else:
    ec2_client.start_instances(InstanceIds=[instance_id])
    print(f"Instance with Id {instance_id} is started successfully")
