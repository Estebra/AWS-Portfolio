"""
This script simulates the retrieval of the  operational  status  of varius  AWS services.
"""

def main():
    service = 'EKS'
    
    # Gets the status of the given service above
    service_status = get_service_status(service)
    
    # if the returned value is true it enters the conditional statement to 
    # deside depending on the status of the service
    if service_status:
        print(f"\n{service} service status is '{service_status}'")
    
        if service_status == 'Operational':
            print(f"Performing operation on '{service}'.")
        else: 
            print(f"'{service}' is NOT operational.")
    else:
        print(f"\nService status for '{service}' could not be retrived.")
    
# This creats a dicctionary with some services and their status
def get_service_status(service_name):
    aws_service_statuses = {
        'EC2' : 'Maintenance',
        'S3' : 'Operational',
        'Lambda' : 'Issues Detected',
        'DynamoDB' : 'Operational',
        'RDS' : 'Operational'
    }
    
    # When trying to return the status(value) from the dictionary
    # Catches if the service(key) doesn't exist in the dictionary
    try:
        return aws_service_statuses[service_name]
    except KeyError as ke:
        print(f"Error: {ke}, \nStatus for AWS service '{service_name}' is not available in our records.")
        return None

if __name__ == '__main__':
    main()