import json

import boto3
import botocore
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
client = boto3.client('lambda')

file_extensions = ['.jpg', '.jpeg']


# add permission to invoke function
def add_permission(function_name, bucket_name):
    client.add_permission(
        FunctionName=function_name,
        StatementId='1',
        Action='lambda:InvokeFunction',
        Principal='s3.amazonaws.com',
        SourceArn=f'arn:aws:s3:::{bucket_name}',
    )


def check_bucket(bucket_name):
    try:
        response = s3.head_bucket(Bucket=bucket_name)
    except s3.exceptions.ClientError as ex:
        print(f"bucket {bucket_name} doesn't exist")
        # print(ex)
        create_bucket(bucket_name)
        return False
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    if status_code == 200:
        return True


def create_bucket(bucket_name):
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} was created successfully")
    except Exception as ex:
        print(ex)


def create_s3_trigger(bucket_name, function_name):
    check_bucket(bucket_name)
    if not bucket_policy_exist(bucket_name):
        create_bucket_policy(bucket_name)

    lambda_response_data = []
    for extension in file_extensions:
        lambda_response_data.append({
            'LambdaFunctionArn': client.get_function(
                FunctionName='lambda_process')['Configuration']['FunctionArn'],
            'Events': [
                's3:ObjectCreated:*'
            ],
            'Filter': {
                'Key': {
                    'FilterRules': [
                        {
                            'Name': 'suffix',
                            'Value': extension
                        },
                    ]
                }
            }
        }, )
    try:
        add_permission(function_name, bucket_name)
        s3.put_bucket_notification_configuration(
            Bucket=bucket_name,
            NotificationConfiguration={
                'LambdaFunctionConfigurations': lambda_response_data,
            }
        )
        print(f'{function_name} has been added to {bucket_name}')
    except ClientError as e:
        print(e)


def bucket_policy_exist(bucket_name):
    try:
        response = s3.get_bucket_policy(Bucket=bucket_name)
        return True
    except botocore.exceptions.ClientError as ex:
        # print(ex)
        return False


def create_bucket_policy(bucket_name):
    if bucket_policy_exist(bucket_name):
        print(f"bucket {bucket_name}'s policy already exists")
    else:
        s3.put_bucket_policy(
            Bucket=bucket_name,
            Policy=generate_policy(bucket_name)
        )
        print("Bucket policy created successfully")


def generate_policy(bucket_name):
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "Allow",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:*",
                "Resource": f"arn:aws:s3:::{bucket_name}/*"
            }
        ]
    }

    return json.dumps(policy)


def main():
    create_s3_trigger('test-bucket99611234', 'lambda_process')


if __name__ == '__main__':
    main()
