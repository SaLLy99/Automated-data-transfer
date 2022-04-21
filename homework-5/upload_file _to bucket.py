import boto3


s3 = boto3.client('s3')
s3_client = boto3.resource('s3')


def upload_file_put(file_path, bucket_name, file_name):
    try:
        s3_client.meta.client.upload_file(Filename=file_path, Bucket=bucket_name, Key=file_name)
        print(f"file {file_name} uploaded to bucket {bucket_name}")
    except s3.exceptions.ClientError as ex:
        print(ex)


def main():
    upload_file_put("photos/dog.jpg", "test-bucket99611234", "dog.jpg")


if __name__ == "__main__":
    main()
