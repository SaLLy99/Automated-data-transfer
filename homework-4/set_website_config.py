import argparse
from os import getenv
from pprint import pprint

import boto3
from botocore.config import Config

AWS_REGION = getenv("AWS_REGION", "us-east-1")
CUSTOM_CONFIG = Config(region_name=AWS_REGION)
s3 = boto3.client("s3", config=CUSTOM_CONFIG)


def set_website_config(bucket_name):
    response = s3.put_bucket_website(
        Bucket=bucket_name,
        WebsiteConfiguration={
            "ErrorDocument": {
                "Key": "error.html"
            },
            "IndexDocument": {
                "Suffix": "index.html"
            }
        }

    )
    pprint(response)
    print_bucket_url(bucket_name)


def main():
    args = parse_args()
    set_website_config(args.bucket)


def print_bucket_url(bucket_name):
    location = s3.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
    key = ""
    url = "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, key)
    print(f"website address:{url}")


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
