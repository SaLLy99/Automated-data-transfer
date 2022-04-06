import argparse
import mimetypes
import os
from os import getenv
import boto3
from botocore.config import Config

AWS_REGION = getenv("AWS_REGION", "us-east-1")
CUSTOM_CONFIG = Config(region_name=AWS_REGION)
s3 = boto3.client("s3", config=CUSTOM_CONFIG)


def guess_type(dir_path):
    mimetype, _ = mimetypes.guess_type(dir_path)
    if mimetype is None:
        return "binary/octet-stream"
    return mimetype


def upload_directory(dir_path, bucket_name):
    for root, _, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            print("Uploading....", file_path)
            s3.upload_file(file_path,
                           bucket_name,
                           file_path.replace(f"{dir_path}/", ""),
                           ExtraArgs={
                               "ContentType": guess_type(file_path)
                           })


def main():
    args = parse_args()
    upload_directory(args.dir, args.bucket)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bucket",
                        type=str,
                        help="S3 bucket name",
                        required=True)
    parser.add_argument("-d", "--dir",
                        type=str,
                        help="Path to directory",
                        required=True)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
