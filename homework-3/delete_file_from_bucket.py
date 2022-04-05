import boto3

s3 = boto3.client('s3')


def delete_file(bucket_name, file_name):
    try:
        s3.delete_object(Bucket=bucket_name, Key=file_name)
        print(f"file {file_name} was deleted successfully")
    except Exception as ex:
        print(str(ex))


def main():
    delete_file("test-bucket99611234", "tmp/upload/one.txt")


if __name__ == "__main__":
    main()
