import boto3

# Create a session using your AWS credentials
session = boto3.Session(
aws_access_key_id = "AKIA4NYMPNXIOL2WFACG",
aws_secret_access_key = "adAnB1zDDoMGIC0Qq9w6EV83YZfRVuVB/y5iqdQP",
    region_name='us-east-1'
)

# Create an EC2 client
ec2_client = session.client('ec2')

# Define the parameters for the instance
instance_params = {
    'ImageId': 'ami-06ca3ca175f37dd66',  # Replace with the desired AMI ID
    'InstanceType': 't2.micro',  # Replace with the desired instance type
    'KeyName': 'demo_instance',  # Replace with the name of your key pair
    'MinCount': 1,
    'MaxCount': 1
}

# Create the instance
response = ec2_client.run_instances(**instance_params)

# Get the instance ID
instance_id = response['Instances'][0]['InstanceId']

print(f"Instance created with ID: {instance_id}")
