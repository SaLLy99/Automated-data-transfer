import json
import secrets
import string
from pprint import pprint

import boto3
import re
import json

iam_client = boto3.client("iam")
password = 'aGVsbG8='


def create_user(user_name):
    response = iam_client.create_user(
        UserName=user_name,
    )
    user_id = response.get('User').get('UserId')
    iam_client.create_login_profile(
        UserName=user_name,
        Password=password,
        PasswordResetRequired=False
    )
    print(f'user by following user name {user_name} created')

    return user_id


def create_group(group_name):
    response = iam_client.create_group(GroupName=group_name)

    print(response)
    return group_name


def assign_policy_to_group(group_name, policy_arn):
    response = iam_client.attach_group_policy(GroupName=group_name, PolicyArn=policy_arn)
    print(response)


def add_user_to_group(user_name, group_name):
    response = iam_client.add_user_to_group(GroupName=group_name, UserName=user_name)
    pprint(response)


def create_authorization_data(user_name, password, usr_id):
    dictionary = {
        "usr_id": usr_id,
        "user_name": user_name,
        "password": password
    }

    # Serializing json
    json_object = json.dumps(dictionary, indent=4)

    # Writing to sample.json
    with open("cred.json", "w") as outfile:
        outfile.write(json_object)


def main():
    user_name = "test_user"
    group_name = "Admins"
    user_id = create_user(user_name)
    create_group(group_name)
    policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
    assign_policy_to_group(group_name, policy_arn)
    add_user_to_group(user_name, group_name)
    create_authorization_data(user_name, password, user_id)


if __name__ == '__main__':
    main()
