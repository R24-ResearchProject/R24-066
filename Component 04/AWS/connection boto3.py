import boto3
import os

# Initialize the S3 client
s3 = boto3.client('s3')

# Specify your bucket name
BUCKET_NAME = 'testminindu'
PREFIX = '/Users/minu/Desktop/R24-066/Component 04/AWS/S3 ' 
LOCAL_DOWNLOAD_PATH = '/Users/minu/Desktop/R24-066/Component 04/AWS/defect images'

# List and download images
objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
for obj in objects.get('Contents', []):
    file_name = obj['Key'].split('/')[-1]
    s3.download_file(BUCKET_NAME, obj['Key'], os.path.join(LOCAL_DOWNLOAD_PATH, file_name))
