import csv # handls CVS files
import boto3 # AWS SDK
from datetime import datetime

"""
# THIS IS PART OF THE HOL 22 -------------------------------------------------------

def get_international_taxes(valid_product_lines, billing_bucket, csv_file):
    try:
        raise Exception("API failure: Internation Taxes API is currently unavailable.")
    except Exception as error:
        sns = boto3.client('sns')
        sns_topic_arn = 'arn:aws:sns:us-east-1:869014851264:TaxesAPIConnectionError'
        message = f"Lambda function failed to reach international takes API for '{billing_bucket}' bucket and file '{csv_file}'. Error: '{error}'."
        sns.publish(
            TopicArn = sns_topic_arn,
            Message = message,
            Subject = "Lambda API Call Failure"
            )
        print("Published failure to sns topic.")
        raise error
        
    # HERE FINISHES THE PART OF THE HOL 22 ---------------------------------------------
"""

def lambda_handler(event, context):
    # Initialize the S3 resource using Boto3
    s3 = boto3.resource('s3')
    
    # Extract the bucket name and the CSV file name from the event input (event.json)
    billing_bucket = event['Records'][0]['s3']['bucket']['name']
    csv_file = event['Records'][0]['s3']['object']['key']
    
    # Define name of the error bucket where you want to copy the erroneus CSV files
    error_bucket = 'dct-billing-errors-01' # This is the name of the S3 bucket  
    # THIS IS PART OF THE HOL 22 -------------------------------------------------------
    processed_bucket = 'dct-billing-processed-022'
    # HERE FINISHES THE PART OF THE HOL 22 ---------------------------------------------
    
    # Download the CVS file from the S3, read the content, decode from bytes to strings, and split the content in lines 
    obj = s3.Object(billing_bucket, csv_file)
    data = obj.get()['Body'].read().decode('utf-8').splitlines()
    
    # Initialize  a flag (error_found) to fase. will be set to true when error is found
    error_found = False
    
    # Define valid product lines and valid currencies
    valid_product_lines = ['Bakery', 'Meat', 'Dairy']
    valid_currencies = ['USD', 'MXN', 'CAD']
    
    """
    # THIS IS PART OF THE HOL 22 -------------------------------------------------------
    get_international_taxes(valid_product_lines, billing_bucket, csv_file)
    # HERE FINISHES THE PART OF THE HOL 22 ---------------------------------------------
    """
    
    # Read the CSV content line by line using Python's CSV reader, ignoring header line (data[1:])
    for row in csv.reader(data[1:]):
        #print(f"{row}")
        # For eac row, extract the product line, currency, bill amount, and date from the specific columns
        date = row[6]
        currency = row[7]
        bill_amount = float(row[8])
        product_line = row[4]
        
        # Check if the product line is valid. if not, set error flag to true and print an error message
        if product_line not in valid_product_lines:
            error_found = True
            print(f"Error in record {row[0]}, invalid product: {product_line}.")
            break
        
        # Check if the currency is valid. if not, set error flag to true and print an error message
        if currency not in valid_currencies:
            error_found = True
            print(f"Error in record {row[0]}, invalid currenty: {currency}.")
            break
        
        # Check if the bill amount si negative. if so, set error flag to true and print an error message
        if bill_amount < 0:
            error_found = True
            print(f"Error in record {row[0]}, bill amount is not a valid amount: {bill_amount}.")
        
        # Check if the date is in the correct format ('%Y-%m-%d'). if not, set error flag to true and print an error message
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            error_found = True
            print(f"Error in record {row[0]}, incorrect date format: {date}.")
            break
        
    # After checking all rows, if an error is found, copy the CSV fgile to the error bucket and delete it from the original bucket
    if error_found:
        copy_source = { # Dictionary and pass it to Boto3 in order to copy the file and transfer it over the error buckte
            'Bucket': billing_bucket,
            'Key': csv_file
        }
        try:
            s3.meta.client.copy(copy_source, error_bucket, csv_file)
            print(f"Moved erronous file to: {error_bucket}")
        
            # Now we want to delete the csv file 
            s3.Object(billing_bucket, csv_file).delete()
            print(f"Deleted original file from bucket {billing_bucket}")
        except Exception as e:
                print(f"Error while moving file: {str(e)}.")
        
    
        # Handle any exception that may occur wihle moving the file, and print the error message
        
    # If no errors were found, return a success message with status code 200 and a bodyy message indicating that no errors were found
    else:
        # THIS IS PART OF THE HOL 22 -------------------------------------------------------
        copy_source = {
            'Bucket': billing_bucket,
            'Key': csv_file
        }
        try:
            s3.meta.client.copy(copy_source, processed_bucket, csv_file)
            print(f"Moved processed file to: {processed_bucket}")
        
            # Now we want to delete the csv file 
            s3.Object(billing_bucket, csv_file).delete()
            print(f"Deleted original file from bucket {billing_bucket}")
        except Exception as e:
                print(f"Error while moving file: {str(e)}.")
        # HERE FINISHES THE PART OF THE HOL 22 ---------------------------------------------