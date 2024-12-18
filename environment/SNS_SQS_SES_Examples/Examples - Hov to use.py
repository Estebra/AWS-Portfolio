import boto3

# SNS example
sns = boto3.client('sns')
response = sns.publish(
    TopicArn = "arn:aws:sns:us-east-1:123456789012:NameoftheTopicARN",
    Message = "This is the message you want to send",
    Subject = "Subject of the message_"
    )
    
    
# SQN example
sqs = boto3.client('sqs')

while True:
    response = sqs.receive_message(
        QueueUrl = 'https://sqs.us-east-1.amazonaws.com/123456789012/NameOfTheQueue',
        MaxNumberOfMessages = 1,
        WaitTimeSeconds = 20
        )
        
    if 'Messages' in response:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
            
        # Process the message here...
            
        sqs.delete_message(
            QueueUrl = 'https://sqs.us-east-1.amazonaws.com/123456789012/NameOfTheQueue',
            ReceiptHandle = receipt_handle
            )
                
# SES Example
ses = boto3.client('ses')

ses.send_email(
    Source = 'no-reply@email-example.org',
    Destination = {
     'ToAddresses': [order_details['destination_email']]   
    },
    Message = {
        'Subject': {
            'Data': email_subject,
            'Charset': 'UTF-8'
        },
        'Body': {
            'Text': {
                'Data': email_body,
                'Charset': 'UTF-8'
            }
        }
    }
)