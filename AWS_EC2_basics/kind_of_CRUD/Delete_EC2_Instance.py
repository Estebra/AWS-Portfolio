"""
This script manages Amazon EC2 instances using the Boto3 Python SDK
"""
# import stamtements
import boto3

# create a EC2 resource and a instance name
ec2 = boto3.resource('ec2')
instance_name = input('Input the name of the EC2 instance to be deleted: ')

# store instance id
instance_id = None

# Check whether the instance you're trying to create is already created
# and only work with an instance that hasn't been terminated
instances = ec2.instances.all()
instance_exist = False

for instance in instances:
    for tag in instance.tags:
        if tag['Key'] == 'Name' and tag['Value'] == instance_name:
            instance_exist = True
            instance_id = instance.id
            print(f"An instance named '{instance_name}' with the ID of '{instance_id}' exists.")
            break

if instance_exist:
    # Delete snapshot
    ec2.Instance(instance_id).terminate()
    print(f"Instance '{instance_name}'-'{instance_id}' has been terminated.")
else:
    print(f"Instance '{instance_name}' does not exist")
