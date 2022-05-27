from os import getenv

import boto3

#AWS_REGION = getenv("AWS_REGION", "eu-east-1")
#dynamodb = boto3.resource("dynamodb", region_name="eu-east-1")
#Lab works without specifying region
dynamodb = boto3.resource("dynamodb")
client = boto3.client("dynamodb")


def print_dynamo_tables():
    tables = list(dynamodb.tables.all())
    print(f'here are tables:{tables}')


def main():
    print_dynamo_tables()


if __name__ == '__main__':
    main()
