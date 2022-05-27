import argparse
from pprint import pprint

import boto3

rds_client = boto3.client('rds')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--instance", type=str, help="Instance id", required=True)
    args = parser.parse_args()
    return args


def upgrade_db_instance_memory(identifier):
    response = rds_client.describe_db_instances(DBInstanceIdentifier=identifier)
    instance = response.get("DBInstances")[0]
    # get current memory
    current_allocated_storage = instance.get('AllocatedStorage')
    upgraded_storage = current_allocated_storage + current_allocated_storage * 0.25
    converted_storage_value = int(upgraded_storage)
    print(converted_storage_value)
    result = rds_client.modify_db_instance(
        DBInstanceIdentifier=identifier,
        AllocatedStorage=converted_storage_value
    )
    pprint(result)


def main():
    args = parse_args()
    upgrade_db_instance_memory(args.instance)


if __name__ == "__main__":
    main()
