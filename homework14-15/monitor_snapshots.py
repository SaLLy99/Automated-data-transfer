import datetime
import boto3

ec2_client = boto3.client("ec2")
day_limit = 3


def calculate_day_difference(date):
    date_obj = date.replace(tzinfo=None)
    diff = datetime.datetime.now() - date_obj
    return diff.days


def list_snapshots():
    response = ec2_client.describe_snapshots(OwnerIds=["self"])
    volumes = response.get("Snapshots")
    print(volumes)


def delete_old_snapshots():
    response = ec2_client.describe_snapshots(OwnerIds=[
        'self'
    ])
    for item in response['Snapshots']:
        create_date = item['StartTime']
        snapshot_id = item['SnapshotId']
        day_old = calculate_day_difference(create_date)
        if day_old > day_limit:
            try:

                print
                "deleting -> " + snapshot_id + " as image is " + str(day_old) + " old."
                # delete the snapshot
                ec2_client.delete_snapshot(SnapshotId=snapshot_id)
            except:
                print
                "can't delete " + snapshot_id


def main():
    list_snapshots()
    delete_old_snapshots()


if __name__ == '__main__':
    main()
