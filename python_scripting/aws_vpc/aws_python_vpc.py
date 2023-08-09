import boto3

session = boto3.Session()
aws_mgmt_cli = boto3.session.Session()
ec2_con_cli = aws_mgmt_cli.client(service_name='ec2')

# Creating a VPC here
my_vpc_cidr_block = '172.168.0.0/16'
my_vpc_name = 'New_VPC'
vpc_response = ec2_con_cli.create_vpc(CidrBlock=my_vpc_cidr_block,
                                      TagSpecifications=[
                                          {
                                              'ResourceType': 'vpc',
                                              'Tags': [{'Key': 'Name', 'Value': my_vpc_name}]
                                          }
                                      ]
                                      )
my_vpc_id = vpc_response['Vpc']['VpcId']
print('VPC ' + my_vpc_name + ' created ' + my_vpc_id)

# Create an Internet Gateway
my_igw_name = 'New_IGW'
igw_response = ec2_con_cli.create_internet_gateway(
    TagSpecifications=[{
        'ResourceType': 'internet-gateway',
        'Tags': [{
            'Key': 'Name',
            'Value': my_igw_name
        }]
    }]
)
my_igw_id = igw_response['InternetGateway']['InternetGatewayId']
print('Internet Gateway ' + my_igw_name + ' created ' + my_igw_id)

# Attach Internet Gateway with VPC ID
ec2_con_cli.attach_internet_gateway(InternetGatewayId=my_igw_id, VpcId=my_vpc_id)
print('InternetGateway ' + my_igw_name + ' is attached with VPC ' + my_vpc_name)

# Create a Public Subnet
my_subnet_cidr_block = '172.168.28.0/24'
my_pub_subnet_name = 'New_pub_subnet'
subnet_response = ec2_con_cli.create_subnet(
    AvailabilityZone='us-east-1a',
    VpcId=my_vpc_id,
    CidrBlock=my_subnet_cidr_block,
    TagSpecifications=[{
        'ResourceType': 'subnet',
        'Tags': [{
            'Key': 'Name',
            'Value': my_pub_subnet_name
        }]
    }]
)
my_subnet_id = subnet_response['Subnet']['SubnetId']
print('Public Subnet ' + my_pub_subnet_name + ' created ' + my_subnet_id)

# Create a Private Subnet
my_subnet_cidr_block_p = '172.168.23.0/24'
my_pri_subnet_name = 'New_pri_subnet'
subnet_response = ec2_con_cli.create_subnet(
    AvailabilityZone='us-east-1a',
    VpcId=my_vpc_id,
    CidrBlock=my_subnet_cidr_block_p,
    TagSpecifications=[{
        'ResourceType': 'subnet',
        'Tags': [{
            'Key': 'Name',
            'Value': my_pri_subnet_name
        }]
    }]
)
my_subnet_id_p = subnet_response['Subnet']['SubnetId']
print('Private Subnet ' + my_pri_subnet_name + ' created ' + my_subnet_id_p)

# Create a custom route table
my_rtb_name = 'New_route_table'
rtb_response = ec2_con_cli.create_route_table(
    VpcId=my_vpc_id,
    TagSpecifications=[{
        'ResourceType': 'route-table',
        'Tags': [{
            'Key': 'Name',
            'Value': my_rtb_name
        }]
    }]
)
my_rtb_id = rtb_response['RouteTable']['RouteTableId']
print('RouteTable ' + my_rtb_id + ' for VPC ' + my_vpc_id + ' is created')

# Add Internet Gateway to the route table
ec2_con_cli.create_route(
    RouteTableId=my_rtb_id,
    GatewayId=my_igw_id,
    DestinationCidrBlock='0.0.0.0/0'
)
print('Internet Gateway ' + my_igw_id + ' is added to the Custom Route Table ' + my_rtb_id)

# Associate subnet into route table
ec2_con_cli.associate_route_table(
    SubnetId=my_subnet_id,
    RouteTableId=my_rtb_id,
)
print('Subnet ' + my_subnet_id + ' is associated with the route table ' + my_rtb_id)

# Allocate an Elastic IP address for NAT Gateway
my_elastic_name = 'New_Elastic_IP'
alloc_response = ec2_con_cli.allocate_address()
alloc_id = alloc_response['AllocationId']
print('Elastic IP address ' + alloc_id + ' allocated')

# Create NAT Gateway for Private Subnet
my_nat_name = 'New_NAT'
nat_res = ec2_con_cli.create_nat_gateway(
    AllocationId=alloc_id,
    SubnetId=my_subnet_id_p,
    TagSpecifications=[{
        'ResourceType': 'natgateway',
        'Tags': [{
            'Key': 'Name',
            'Value': my_nat_name
        }]
    }]
)

# Wait for NAT Gateway to be available
nat_id = nat_res['NatGateway']['NatGatewayId']
waiter = ec2_con_cli.get_waiter('nat_gateway_available')
waiter.wait(NatGatewayIds=[nat_id])
print('NAT Gateway ' + my_nat_name + ' ' + nat_id + ' created')

# Find ID for Main Route Table
rtb_response = ec2_con_cli.describe_route_tables(Filters=[
    {'Name': 'vpc-id', 'Values': [my_vpc_id]},
    {'Name': 'association.main', 'Values': ['true']}
])
for each_rtb in rtb_response['RouteTables']:
    for each_association in each_rtb['Associations']:
        main_rtb_id = each_association['RouteTableId']

# Add Tags to Main Route Table
main_rtb_name = 'Retail_Main_RTB'
ec2_con_cli.create_tags(Resources=[main_rtb_id], Tags=[{'Key': 'Name', 'Value': main_rtb_name}])
print('Tag ' + main_rtb_name + ' added to the main Route Table ' + main_rtb_id)

# Add NAT to the main Route Table
ec2_con_cli.create_route(RouteTableId=main_rtb_id, NatGatewayId=nat_id, DestinationCidrBlock='0.0.0.0/0')
print('NAT Gateway ' + nat_id + ' added to the main Route Table ' + main_rtb_id)
