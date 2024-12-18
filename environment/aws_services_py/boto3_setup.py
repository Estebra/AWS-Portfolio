import boto3

# Create a resource
s3 = boto3.resource('s3')

# Loop through the buckets
for bucket in s3.buckets.all():
    print(bucket.name)