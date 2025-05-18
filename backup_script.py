import os
import boto3
from datetime import datetime
import hashlib
import schedule
import time

def calculate_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def backup_file(file_path, bucket_name):
    s3 = boto3.client('s3', aws_access_key_id='YOUR_KEY', aws_secret_access_key='YOUR_SECRET')
    file_name = os.path.basename(file_path)
    file_hash = calculate_hash(file_path)
    backup_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    s3_key = f"{file_hash}_{backup_time}_{file_name}"
    s3.upload_file(file_path, bucket_name, s3_key)
    print(f"Uploaded to S3: {bucket_name}/{s3_key}")

def job():
    file_path = "sample.txt"  # Change this path to your file
    bucket_name = "your-bucket-name"  # Change this to your bucket
    print(f"Starting backup process for file: {file_path}")
    backup_file(file_path, bucket_name)
    print("Backup completed successfully!")

# Schedule backup every day at midnight
schedule.every().day.at("00:00").do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)