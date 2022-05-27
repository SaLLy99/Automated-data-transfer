import boto3

ec2_client = boto3.client("ec2")
VPC_ID = "vpc-01c0dc9cce75986b9"  # Last vpc


def create_key_pair(key_name):
    response = ec2_client.create_key_pair(
        KeyName=key_name,
        KeyType="rsa"
        # KeyFormat="pem"
    )
    key_id = response.get("KeyPairId")
    with open(f"{key_name}.pem", "w") as file:
        file.write(response.get("KeyMaterial"))
    print("Key pair id - ", key_id)
    return key_id


def create_security_group(name, description):
    response = ec2_client.create_security_group(
        Description=description,
        GroupName=name,
        VpcId=VPC_ID)
    group_id = response.get('GroupId')

    print('Security Group Id - ', group_id)

    return group_id


def add_all_access_sg(sg_id):
    response = ec2_client.authorize_security_group_ingress(
        CidrIp='0.0.0.0/0',
        FromPort=80,
        GroupId=sg_id,
        IpProtocol='tcp',
        ToPort=80,
    )
    if response.get('Return'):
        print('Rule added successfully')
    else:
        print('Rule was not added')


def add_postrgress_access_sg(sg_id):
    response = ec2_client.authorize_security_group_ingress(
        CidrIp='0.0.0.0/0',
        FromPort=3306,
        GroupId=sg_id,
        IpProtocol='tcp',
        ToPort=3306,
    )
    if response.get('Return'):
        print('Rule added successfully')
    else:
        print('Rule was not added')


def create_db_instance(sg_id):
    rds_client = boto3.client('rds')
    response = rds_client.create_db_instance(
        DBName='btu',
        DBInstanceIdentifier='btu-pg-1',
        AllocatedStorage=60,
        DBInstanceClass='db.t4g.micro',
        Engine='mysql',
        MasterUsername='btu',
        MasterUserPassword='strongestpassword',
        VpcSecurityGroupIds=[
            sg_id,
        ],
        BackupRetentionPeriod=7,
        Port=3306,
        MultiAZ=False,
        EngineVersion='8.0',
        AutoMinorVersionUpgrade=True,
        # Iops=123, # Necessary when StorageType is 'io1'
        PubliclyAccessible=True,
        Tags=[
            {
                'Key': 'Name',
                'Value': 'BTU PG DB'
            },
        ],
        StorageType='gp2',
        EnablePerformanceInsights=True,
        PerformanceInsightsRetentionPeriod=7,
        DeletionProtection=False,
    )
    _id = response.get('DBInstance').get('DBInstanceIdentifier')
    print(f'Instance {_id} was created')


def main():
    # scuerity group configuraiton
    create_key_pair("my-demo_key")
    sg_id = create_security_group('ec2-sg', 'Security group to enable access on ec2')
    print('security group id ' + sg_id)
    add_all_access_sg(sg_id)
    add_postrgress_access_sg(sg_id)
    # rds configuration
    create_db_instance(sg_id)


if __name__ == '__main__':
    main()
