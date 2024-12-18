import boto3, time

# Create a EC2 client
ec2 = boto3.client('ec2')

# Create a name for the VPC
vpc_name = input('Give a name to the VPC: ')

#  If VPC exists, do not create a new one
response = ec2.describe_vpcs( # Using EC2 client to describe the VPCs in the acount
    Filters = [{'Name' : 'tag:Name', 'Values' : [vpc_name]}] # Filtering for VPCs with 'vpc_name'
    )
vpcs = response.get('Vpcs', [])

if vpcs:
    vpc_id = vpcs[0]['VpcId']
    print(f"VPC '{vpc_name}' with ID '{vpc_id}' already exists")
else:

    # ----------------Create a VPC----------------
    vpc_response = ec2.create_vpc(CidrBlock = '10.0.0.0/16')
    vpc_id = vpc_response['Vpc']['VpcId']
    # Here we can create a dedicated function to see when the VPC is created
    # For now a short delay is added
    time.sleep(5)
    ec2.create_tags(Resources = [vpc_id], Tags = [{'Key' : 'Name', 'Value' : vpc_name}])
    print(f"VPC '{vpc_name}' with ID '{vpc_id}' has been created.")


# ----------------Create a internet gateway----------------

# Name of the internet gateways
ig_name = input('Give the internet gateways a name: ')#'intGate-vpc-from-boto'

#  If a Internet Gateway exists, do not create a new one
response = ec2.describe_internet_gateways( # Using EC2 client to describe the internet gateways in the acount
    Filters = [{'Name' : 'tag:Name', 'Values' : [ig_name]}] # Filtering for internet gateways with 'ig_name'
    )
internet_gateways = response.get('InternetGateways', [])

if internet_gateways:
    ig_id = internet_gateways[0]['InternetGatewayId']
    print(f"Internet Gateway '{ig_name}' with ID '{ig_id}' already exists")
else:

    # ----------------Create a VPC----------------
    ig_response = ec2.create_internet_gateway()
    ig_id = ig_response['InternetGateway']['InternetGatewayId']
    # Here we can create a dedicated function to see when the VPC is created
    # For now a short delay is added
    time.sleep(5)
    ec2.create_tags(Resources = [ig_id], Tags = [{'Key' : 'Name', 'Value' : ig_name}])
    
    # Attach the Internet Gateway to the VPC
    ec2.attach_internet_gateway(VpcId = vpc_id, InternetGatewayId = ig_id)
    
    print(f"Inernet Gateway '{ig_name}' with ID '{ig_id}' has been created.")



# ----------------Create a  route table and a public route----------------

# Get a Route table response
rt_response = ec2.create_route_table(VpcId = vpc_id)
#Get the route table ID
rt_id = rt_response['RouteTable']['RouteTableId']
# Route to the internet
route = ec2.create_route(
    RouteTableId = rt_id,
    DestinationCidrBlock ='0.0.0.0/0', # to route it to the internet
    GatewayId = ig_id
    )
print(f"Route table wih ID '{rt_id}' as been created.")

# ----------------Create 3 subnets----------------
subnet_1 = ec2.create_subnet(VpcId = vpc_id, CidrBlock = '10.0.1.0/24', AvailabilityZone = 'us-east-1a')
subnet_2 = ec2.create_subnet(VpcId = vpc_id, CidrBlock = '10.0.2.0/24', AvailabilityZone = 'us-east-1b')
subnet_3 = ec2.create_subnet(VpcId = vpc_id, CidrBlock = '10.0.3.0/24', AvailabilityZone = 'us-east-1c')

print(f"Subnet_1 ID = '{subnet_1['Subnet']['SubnetId']}', Subnet_2 ID = '{subnet_2['Subnet']['SubnetId']}', Subnet_3 ID = '{subnet_3['Subnet']['SubnetId']}'")