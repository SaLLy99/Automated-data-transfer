import argparse

import boto3

client = boto3.client("rds")


def create_backup(identifier):
    response = client.create_db_snapshot(
        DBSnapshotIdentifier=f"{identifier}-final-snapshot",
        DBInstanceIdentifier=identifier,
        Tags=[
            {
                'Key': 'Name',
                'Value': 'BTU db snapshot'
            },
        ]
    )
    print(response)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--instance", type=str, help="Instance id", required=True)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    create_backup(args.instance)


if __name__ == '__main__':
    main()
