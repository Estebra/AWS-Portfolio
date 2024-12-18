def main():
    
    aws_services = ['S3', 'Lambda', 'EC2', 'RDS', 'DynamoDB']
    print(f'AWS services list: {aws_services}')
    
    print(f'\nUsing enumerate() with a for loop to get both index and value:')
    
    for index, value in enumerate(aws_services):
        print(f'AWS service index: {value} : {index}')


if __name__ == '__main__':
    main()