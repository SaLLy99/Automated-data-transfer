from datetime import datetime

import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')


def upload_file_with_new_version(bucket_name, file_name):
    # Get a list of all versions contained in the bucket
    try:
        versions = s3.list_object_versions(Bucket=bucket_name, Prefix=file_name)
    except ClientError as e:
        raise Exception("boto3 client error in list_all_objects_version function: " + e.__str__())
    except Exception as e:
        raise Exception("Unexpected error in list_all_objects_version function of s3 helper: " + e.__str__())
    i = 0

    # Versions['Versions'] is sorted and we need to get version id of the element which  was modified before last
    # modification
    versions_length = len(versions['Versions'])
    while i < versions_length-1:
        version_id = versions['Versions'][i]['VersionId']
        file_key = versions['Versions'][i]['Key']
        i = i + 1

    response = s3.get_object(
        Bucket=bucket_name,
        Key=file_key,
        VersionId=version_id,
    )
    data = response['Body'].read()

    create_file_with_older_version(file_name, data)
    upload_file_put(bucket_name, file_name)


def create_file_with_older_version(file_name, data):
    with open(file_name, "wb") as file:
        file.write(data)


def upload_file_put(bucket_name, file_name):
    try:
        with open(file_name, "rb") as file:
            s3.put_object(Bucket=bucket_name, Key=file_name, Body=file.read())
        print(f"file {file_name} uploaded to bucket {bucket_name}")
    except s3.exceptions.ClientError as ex:
        print(ex)


def main():
    upload_file_with_new_version("test-bucket99611234", "tmp/upload/one.txt")


if __name__ == "__main__":
    main()
