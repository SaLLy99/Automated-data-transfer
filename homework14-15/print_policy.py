import argparse
from pprint import pprint

import boto3

iam_client = boto3.client("iam")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", type=str, help="Username", required=True)
    args = parser.parse_args()
    return args


def print_user_policy(username):
    response = iam_client.list_user_policies(
        UserName=username
    )
    policy_names = response.get('PolicyNames')
    print(policy_names)


def main():
    args = parse_args()
    print_user_policy(args.username)


if __name__ == '__main__':
    main()
