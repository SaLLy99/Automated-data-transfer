import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')


def check_bucket(bucket_name):
    try:
        response = s3.head_bucket(Bucket=bucket_name)
    except s3.exceptions.ClientError as ex:
        print(f"bucket {bucket_name} doesn't exist")
        # print(ex)
        return False
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    if status_code == 200:
        bucket_delete(bucket_name)
        return True


def bucket_delete(bucket_name):
    try:
        # bucket = boto3.resource('s3').Bucket(bucket_name)
        # bucket.objects.all().delete()
        # bucket.delete()
        s3.delete_bucket(Bucket=bucket_name)
        print(f"bucket {bucket_name} deleted")
    except ClientError as e:
        print(e)


def main():
    check_bucket('test-bucket99611234')


if __name__ == "__main__":
    main()
