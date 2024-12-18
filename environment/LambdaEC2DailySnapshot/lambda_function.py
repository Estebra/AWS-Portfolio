import json
import boto3
import logging
from datetime import datetime

# Setup of the ligging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# This is the entry point into the lambda function
def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    #SNAPSHOT PROCEDURE
    
    try:
        response = ec2.create_snapshot(
            # This is the parameter set
            VolumeId='vol-041d488fd14996968', # this is in the AWS console
            Description='Daily EC2 Snapshot',
            TagSpecifications=[
                {
                    'ResourceType': 'snapshot',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': f"EC2 Snapshot {current_date}"
                            }
                        ]
                    }
                ]
            
            )
            
        logger.info(f"Successfully created sapshot: {json.dumps(response, default=str)}")
        
    except Exception as e:
        logger.error(f"Error creating snapshot: {str(e)}")