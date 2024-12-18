import boto3
import io
import csv
import logging

# Constants - database and credentials details, and currency conversion rates
currency_conversion_to_usd = {'USD' : 1, 'CAD' : .79, 'MXN' : .05}
database_name = 'rds_AutomatingRDSwithLambda_db' # this should not be the cluster name
secret_store_arn = 'arn:aws:secretsmanager:us-east-1:869014851264:secret:rds-db-credentials/cluster-C2EYESDCT2EMULWG3QVERHLHVA/dctuser21/1726817700577-SI3PTE'
db_cluster_arn = 'arn:aws:rds:us-east-1:869014851264:cluster:rds-automatingrdswithlambda-cluster'

# Boto3 clients for AWS services
s3_client = boto3.client('s3')
rds_client = boto3.client('rds-data')

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Function to process each record/row from the CSV file
def process_record(record):
    id, company_name, country, city, product_line, item, bill_date, currency, bill_amount = record
    bill_amount = float(bill_amount) 

    # Convert the bill amount to USD ussing conversion rates
    usd_amount = 0
    rate = currency_conversion_to_usd.get(currency)
    if rate:
        usd_amount = rate * bill_amount
        
    # If no conversion rate is found for the currency, log and info message    
    else:
        logger.info(f"No rate found for currency: {currency}")
        
    #print(f"ID: {id} currency: {currency} rate: {rate}.") # This is test print to see the data we are processing
    
    # Prepare SQL  statement with placeholders for inserting record into the database
    sql_statement = ("INSERT IGNORE INTO billing_data" # this is the name of the table 
                        "(id, company_name, country, city, product_line, "
                        "item, bill_date, currency, bill_amount, bill_amount_usd) "
                        "VALUES (:id, :company_name, :country, :city, :product_line, "
                                ":item, :bill_date, :currency, :bill_amount, :usd_amount)"
                    )
    
    # Prepare parameters for SQL statement
    sql_parameters = [
        {'name': 'id', 'value':{'stringValue': id}},
        {'name': 'company_name', 'value':{'stringValue': company_name}},
        {'name': 'country', 'value':{'stringValue': country}},
        {'name': 'city', 'value':{'stringValue': city}},
        {'name': 'product_line', 'value':{'stringValue': product_line}},
        {'name': 'item', 'value':{'stringValue': item}},
        {'name': 'bill_date', 'value':{'stringValue': bill_date}},
        {'name': 'currency', 'value':{'stringValue': currency}},
        {'name': 'bill_amount', 'value':{'doubleValue': bill_amount}},
        {'name': 'usd_amount', 'value':{'doubleValue': usd_amount}}
    ]
    
    # Execute the SQL statement and log the response
    response = execute_statement(sql_statement, sql_parameters)
    logger.info(f"SQL execution response: {response}")
    

# Function to execute SQL  statement
def execute_statement(sql, sql_parameters):
    try:
        response = rds_client.execute_statement(
                secretArn = secret_store_arn,
                database = database_name,
                resourceArn = db_cluster_arn,
                sql = sql,
                parameters = sql_parameters
            )
    except Exception as e:
        logger.error(f"Error: Could not connect to Aurora Serverless MySQL instance: {e}.")
        return None

    # Use RDS Data API to execute the SQL statement
    
    # If an error occurs while connecting to the database, log an error message

def lambda_handler(event, context):
    
    try:
        # Get the bucket name and file name from the event 
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        s3_file = event['Records'][0]['s3']['object']['key']
        
        # Read the file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key = s3_file)
        data = response['Body'].read().decode('utf-8')
        
        # Use csv reader to process the CSV data
        csv_reader = csv.reader(io.StringIO(data))
        next(csv_reader)
        
        # Process each record in the CSV file
        for record in csv_reader:
            #print(record) # This is a test print to see the records
            process_record(record)
    
    except Exception as e:
        # If an unexpected error occurs, log and error message
        logger.error(f"ERROR: unexpected error: {e}")