"""
This script manages Amazon EC2 instances using the Boto3 Python SDK
"""
# import stamtements
import boto3

# create a EC2 resource and a instance name
ec2 = boto3.resource('ec2')
instance_name = 'lambdaEC2DailySnapshot'

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
            print(f"An instance named '{instance_name}' with the ID of '{instance_id}' already exists.")
            break
    if instance_exist:
        break

# Launch a new EC2 instance if it hasn't already been created
if not instance_exist:
    new_instance = ec2.create_instances(
        ImageId = 'ami-051f8a213df8bc089', # you can get this # from the EC2 console we you go to lauch a instance there
        MinCount = 1,
        MaxCount = 1,
        InstanceType = 't2.micro',
        KeyName = 'us-east-kp', # This is your key pair
        TagSpecifications = [
            {
                'ResourceType' : 'instance',
                'Tags' : [
                    {
                        'Key' : 'Name',
                        'Value' : instance_name # this is the name given before
                    },
                ]
            },
        ]
    )
    instance_id = new_instance[0].id
    print(f"Instance named '{instance_name}' with ID '{instance_id}' is created.")

# Stop an instance
#ec2.Instance(instance_id).stop() # Comment this line if already stopped
#print(f"Instance '{instance_name}'-'{instance_id}' has been stopped.")

# Start an instance
#ec2.Instance(instance_id).start() # Comment if already started
#print(f"Instance '{instance_name}'-'{instance_id}' has been started.")

# Terminate an instance
#ec2.Instance(instance_id).terminate()
#print(f"Instance '{instance_name}'-'{instance_id}' has been terminated.")