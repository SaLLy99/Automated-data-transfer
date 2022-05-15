import boto3
import botocore.exceptions

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')


def upload_file_with_new_version(bucket_name, file_name):
    continue_process = check_versioning(bucket_name)
    if not continue_process:
        enable_versioning(bucket_name)
        upload_file_with_new_version(bucket_name, file_name)
    else:
        versions = s3_resource.Bucket(bucket_name).object_versions.filter(Prefix=file_name)
        versions_list = []

        for version in versions:
            obj = version.get()
            print(obj)
            versions_list.append({
                'Key': obj.get('Key'),
                'VersionId': obj.get('VersionId'),
                'LastModified': obj.get('LastModified')
            })
        # sort versions_list by lastModified date
        versions_list.sort(key=lambda x: x['LastModified'])
        # versions_length = len(versions_list)
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=file_name,
            # get one of the last modified object's version id
            VersionId=versions_list[-1]['VersionId'],
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
            s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=file.read())
        print(f"file {file_name} uploaded to bucket {bucket_name}")
    except s3_client.exceptions.ClientError as ex:
        print(ex)


def check_versioning(bucket_name):
    result = False
    for bucket in s3_client.list_buckets()['Buckets']:
        bucket = bucket['Name']
        response = s3_client.get_bucket_versioning(Bucket=bucket)
        if 'Status' in response and response['Status'] == 'Enabled':
            result = True
    return result


def enable_versioning(bucket_name):
    try:
        response = s3_client.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={
                "Status": "Enabled",
            },
        )

        print(f"versioning for bucket {bucket_name} is enabled")

    except botocore.exceptions.ClientError as ex:
        print(ex)


def main():
    upload_file_with_new_version("test-bucket99611234", "tmp/upload/one.txt")


if __name__ == "__main__":
    main()
