import boto3
import pathlib

s3 = boto3.resource('s3')


def list_bucket_by_type(bucket_name):
    my_bucket = s3.Bucket(bucket_name)
    files = my_bucket.objects.all()

    file_list = {}
    file_extensions = []
    # create file's extension list
    for file in files:
        file_extension = pathlib.Path(file.key).suffix
        # remove semicolon from extension and put it into list
        file_extensions.append(file_extension[1:])
    # populate file_list dictionary with file's extension and their amount
    for item in file_extensions:
        file_list[item] = file_extensions.count(item)

    # print file list
    for i in file_list:
        print('{0}-{1}'.format(i, file_list[i]))


def main():
    list_bucket_by_type("test-bucket99611234")


if __name__ == "__main__":
    main()
