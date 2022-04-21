from pathlib import Path

import boto3
import botocore

client = boto3.client('lambda')
iam = boto3.client('iam')


def convert_to_bytes(zip_file):
    with open(zip_file, 'rb') as file_data:
        binary_zip = file_data.read()
    return binary_zip


def create_lambda(function_name, role_name, function_handler, zip_file):
    try:
        client.create_function(Code={
            'ZipFile': convert_to_bytes(zip_file)
        },
            Description='Process image objects from Amazon S3 and creates meta data as a json file'
                        ' after processing.',
            FunctionName=function_name,
            Runtime='python3.8',
            Role=iam.get_role(RoleName=role_name)['Role']['Arn'],
            Handler=f'{Path(zip_file).stem}.{function_handler}'
        )
        print(f'function {function_name} has been created successfully!')
    except botocore.Lambda.Client.exceptions as ex:
        print(ex)


def main():
    create_lambda('lambda_process', 'LabRole',
                  'lambda_handler', './lambda_proces.zip')


if __name__ == "__main__":
    main()
