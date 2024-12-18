import boto3
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ec2_resource = boto3.resource('ec2')
    #test_allocation_id = 'eipalloc-05688055f00419b01'

    try:
        for elastic_ip in ec2_resource.vpc_addresses.all():
            #print(elastic_ip) # Test print to see the EIPs
            if elastic_ip.instance_id is None:
                print(f"\nNo assocciation for elastic IP: {elastic_ip}. Realeasing...\n")
                elastic_ip.release()
                
    except Exception as e:
        logger.error(str(e))
    
    return {
        'statusCode': 200,
        'body': 'Processed elastic IPs'
    }
