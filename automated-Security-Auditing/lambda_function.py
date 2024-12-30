import boto3

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')

    sns_client = boto3.client('sns')
    sns_topic_arn = 'arn:aws:sns:us-east-1:869014851264:DCTSecurityGroupAuditAlerts'
    
    security_groups = ec2.security_groups.all()
    for sg in security_groups:
        print(f"\nChecking security group '{sg.id}' ({sg.group_name}).")
        
        for rule in sg.ip_permissions:
            for ip_range in rule['IpRanges']:
                if ip_range['CidrIp'] == '0.0.0.0/0':
                    message = (f"WARNING: Inbound rule in security group {sg.id} ({sg.group_name})"
                               f" allows traffic from any IP address: \n\n {rule}."
                    )
                    print(message)
                    sns_client.publish(TopicArn=sns_topic_arn, Message=message)

    return {
        'statusCode': 200,
        'body': 'Security audit complete.'
    }
