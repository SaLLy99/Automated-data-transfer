import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')


def delete_file(bucket_name, file_name):
    check_file = file_exist(bucket_name, file_name)
    if not check_file:
        print(f"file {file_name} doesn't exists and can't be deleted")
    else:
        try:
            s3.delete_object(Bucket=bucket_name, Key=file_name)
            print(f"file {file_name} was deleted successfully")
        except ClientError as ex:
            print(ex)


def file_exist(bucket_name, file_name):
    if_exists = False
    try:
        bucket_list = s3.list_objects(Bucket=bucket_name, Prefix=file_name)
        for bucket in bucket_list.get("Contents", []):
            if bucket.get("Key") == file_name:
                if_exists = True

        return if_exists
    except ClientError as ex:
        print(ex)


def main():
    delete_file("test-bucket99611234", "tmp/upload/one.txt")


if __name__ == "__main__":
    main()
