import boto3
import os


def upload_to_s3(file_name, bucket_name="mystocksprediction", s3_key="datasets/stock_price.csv"):
    """
    Uploads a file to an AWS S3 bucket.

    Parameters:
        file_name (str): Path to the local file.
        bucket_name (str): Name of the S3 bucket.
        s3_key (str): Destination path in S3.

    Returns:
        None
    """
    # Initialise an S3 client
    s3 = boto3.client('s3')

    try:
        s3.upload_file(file_name, bucket_name, s3_key)
        print(f"✅ File {file_name} uploaded to {bucket_name}/{s3_key}")
    except Exception as e:
        print(f"❌ Error uploading to S3: {e}")
    

    

