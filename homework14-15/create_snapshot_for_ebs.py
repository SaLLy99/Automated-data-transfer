import boto3

ec2_resource = boto3.resource('ec2')


def create_snapshots():
    for volume_id in ec2_resource.volumes.all():
        snapshot = ec2_resource.create_snapshot(
            VolumeId=volume_id,
            TagSpecifications=[
                {
                    'ResourceType': 'snapshot',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': f'ebs_id:{volume_id}'
                        },
                    ]
                },
            ]
        )
        print(f"snapshot {snapshot.id} has been created")


def main():
    create_snapshots()


if __name__ == '__main__':
    main()
