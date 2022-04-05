import boto3

s3 = boto3.client('s3')


def upload_file_put(bucket_name, file_name):
    try:
        with open(file_name, "rb") as file:
            s3.put_object(Bucket=bucket_name, Key=file_name, Body=file.read())
        print(f"file {file_name} uploaded to bucket {bucket_name}")
    except s3.exceptions.ClientError as ex:
        print(ex)


def main():
    upload_file_put("test-bucket99611234", "tmp/upload/one.txt")


if __name__ == "__main__":
    main()
