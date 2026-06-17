# Upload File to AWS S3 Bucket

import boto3

# Create S3 Client

s3 = boto3.client(
    's3',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    region_name='ap-south-1'
)

try:

    file_name = "sample.txt"
    bucket_name = "your-bucket-name"

    s3.upload_file(
        file_name,
        bucket_name,
        file_name
    )

    print("File Uploaded Successfully")

except Exception as e:
    print("Error:", e)
