import boto3
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Providing the S3 bucket credentials
access_key = os.environ.get('ACCESS_KEY')
secret_access_key = os.environ.get('SECRET_ACCESS_KEY')
bucket_name = os.environ.get('BUCKET_NAME')
aws_region = os.environ.get('REGION')

s3 = boto3.client(
    "s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_access_key,
    region_name= aws_region
)


def upload_images_to_s3(data, filename, bucket_name):
    try:
        s3.upload_fileobj(
            data,
            bucket_name,
            filename
        )

    except Exception as e:
        print(e)
        return "error"

    return "success"
