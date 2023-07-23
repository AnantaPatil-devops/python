"""import boto3

# Create a session using the default profile
session = boto3.Session()

# Create an IAM client using the session
iam_client = session.client('ec2')

# Get current IAM user details
response = iam_client.get_user()

# Extract and print the IAM user name
iam_user_name = response['User']['UserName']
print("IAM User Name:", iam_user_name)
"""
import boto3

# Create a session using your AWS credentials
session = boto3.Session(
aws_access_key_id = "your_Access_keys",
aws_secret_access_key = "aws_secret_access_key",
    region_name='us-east-1'
)

# Create an EC2 client
ec2_client = session.client('ec2')

# Retrieve a list of EC2 instances
response = ec2_client.describe_instances()
print(response)

# Process the response to get the instances
instances = []
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instances.append(instance)

# Display the instance information
for instance in instances:
    instance_id = instance['InstanceId']
    instance_state = instance['State']['Name']
    instance_type = instance['InstanceType']
    ami_id = instance['ImageId']
    print(f"Instance ID: {instance_id}")
    print(f"Instance State: {instance_state}")
    print(f"Instance Type: {instance_type}")
    print(f"AMI ID: {ami_id}")
    print("-----------------------")

