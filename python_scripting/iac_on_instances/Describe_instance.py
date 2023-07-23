import boto3

session=boto3.Session(
    aws_access_key_id = "AKIA4NYMPNXIOCPIVJXK",
    aws_secret_access_key = "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",
    region_name='us-east-1'
)

ec2_client = session.client('ec2')
instance_ids_to_describe =["i-01d73b1ca3eda9ee2"]
response = ec2_client.describe_instances(InstanceIds=instance_ids_to_describe)
print(response)
