import argparse
import json

import boto3
import botocore

s3 = boto3.client('s3')


def bucket_policy_exist(bucket_name):
    try:
        response = s3.get_bucket_policy(Bucket=bucket_name)
        return True
    except botocore.exceptions.ClientError as ex:
        # print(ex)
        return False


def create_bucket_policy(bucket_name):
    if bucket_policy_exist(bucket_name):
        print(f"bucket {bucket_name}'s policy already exists")
    else:
        s3.put_bucket_policy(
            Bucket=bucket_name,
            Policy=generate_policy(bucket_name)
        )
        print("Bucket policy created successfully")


def generate_policy(bucket_name):
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*"
            }
        ]
    }

    return json.dumps(policy)


def main():
    args = parse_args()
    create_bucket_policy(args.bucket)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bucket",
                        type=str,
                        help="S3 bucket name",
                        required=True)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
