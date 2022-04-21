import boto3
import botocore

s3 = boto3.client('s3')


def download_meta_file(bucket_name, file_name, local_directory):
    try:
        s3.download_file(bucket_name, file_name, local_directory)
        print(f'file {file_name} downloaded')
    except botocore.exceptions.ClientError as ex:
        print(ex)


def main():
    download_meta_file("test-bucket99611234", "dog.json", "photos/response.json")


if __name__ == "__main__":
    main()
