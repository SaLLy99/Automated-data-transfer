from os import getenv

import boto3
from botocore.config import Config

AWS_REGION = getenv("AWS_REGION", "us-east-1")
CUSTOM_CONFIG = Config(region_name=AWS_REGION)
s3 = boto3.client("s3", config=CUSTOM_CONFIG)


def create_bucket(bucket_name):
    try:
        if bucket_exist(bucket_name):
            print(f"Bucket {bucket_name} already exists")
        else:
            s3.create_bucket(Bucket=bucket_name)
            # CreateBucketConfiguration={"LocationConstraint": AWS_REGION})
            # lab's api can't create bucket with this parameter  'LocationConstraint'
            # but can work with default region

            print(f"Bucket {bucket_name} was created successfully")
    except Exception as ex:
        print(ex)


def bucket_exist(bucket_name):
    try:
        response = s3.head_bucket(Bucket=bucket_name)
    except s3.exceptions.ClientError as ex:
        # print(ex)
        return False
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    if status_code == 200:
        return True


def main():
    create_bucket('test-bucket99611234')


if __name__ == "__main__":
    main()
