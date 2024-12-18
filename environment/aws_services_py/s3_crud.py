# import the boto3 library
import boto3

# Instatiate a boto3 resource for S3 and name your bucket
s3 = boto3.resource('s3')
bucket_name = 'bucket-test-crud-1'

# Check if bucket already exist 
# Create the bucket if bucket doesn't already exist
all_my_bucket = [bucket.name for bucket in s3.buckets.all()] # This iterates through all the bucket in the account

if bucket_name not in all_my_bucket:
    print(f"'{bucket_name}' bucket doesn't exits.\nCreating now...")
    s3.create_bucket(Bucket = bucket_name)
    print(f"'{bucket_name}' bucket has been created!")
else:
    print(f"'{bucket_name}' already exists, no need to create new one.")

# Create 'file_1.txt' and 'file_2.txt'
# touch file_1.txt file_2.txt
f_1 = 'file_1.txt'
f_2 = 'file_2.txt'

# UPLOAD 'file_1.txt' to the new bucket
s3.Bucket(bucket_name).upload_file(Filename=f_1, Key=f_1)

# READ and print the file from the bucket
obj = s3.Object(bucket_name, f_1)
body = obj.get()['Body'].read()
print(body)

# UPDATE 'file_1.txt' in the bucket with new conten from 'file_2.txt'
s3.Object(bucket_name, f_1).put(Body = open(f_2, 'rb')) # obj.put(Body = open(f_2, 'rb'))
obj = s3.Object(bucket_name, f_1)
body = obj.get()['Body'].read()
print(body)

# DELETE the file from the bucket
s3.Object(bucket_name, f_1).delete() # obj.delete()

# DELETE the bucket (the bucket should be empty)
bucket = s3.Bucket(bucket_name)
bucket.delete()
