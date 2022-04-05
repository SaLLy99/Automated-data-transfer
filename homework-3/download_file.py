import boto3
import botocore
import os

s3 = boto3.client('s3')


def download_file(bucket_name, file_name, local_directory=os.getcwd()+"\\one.txt"):
    try:
        s3.download_file(bucket_name, file_name, local_directory)
        print(f'file {file_name} downloaded')
    except botocore.exceptions.ClientError as ex:
        print(ex)


def main():
    download_file("test-bucket99611234", "tmp/upload/one.txt", "tmp/download/one.txt")
    # download_file("test-bucket99611234", "tmp/upload/one.txt")


if __name__ == "__main__":
    main()
