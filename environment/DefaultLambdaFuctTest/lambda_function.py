import json

def lambda_handler(event, context):
    # Hello from Cloud9
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }