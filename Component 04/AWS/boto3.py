import boto3
from datetime import timezone
from collections import defaultdict, Counter

# Initialize the S3 client
s3 = boto3.client('s3')

# Define the bucket name
bucket_name = 'testminindu'

# Retrieve all objects in the bucket
response = s3.list_objects_v2(Bucket=bucket_name)

# Dictionary to hold counts per day for each defect type
daily_defect_counts = defaultdict(lambda: Counter({'high-low': 0, 'open seam': 0}))

# Process each object in the S3 bucket
for obj in response.get('Contents', []):
    # Get the upload date
    timestamp = obj['LastModified']
    date = timestamp.astimezone(timezone.utc).date()
    
    # Identify the defect type based on file name
    file_key = obj['Key']
    if 'high-low' in file_key:
        defect_type = 'high-low'
    elif 'open seam' in file_key:
        defect_type = 'open seam'
    else:
        continue  # Skip if it's not a high-low or open seam image

    # Increment the count for this defect type and date
    daily_defect_counts[date][defect_type] += 1

# Display results
for date, counts in daily_defect_counts.items():
    print(f"{date}:")
    print(f"  High-Low: {counts['high-low']} images")
    print(f"  Open Seam: {counts['open seam']} images")