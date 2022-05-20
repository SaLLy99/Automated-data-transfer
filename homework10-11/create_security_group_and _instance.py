import socket

import boto3

ec2_client = boto3.client("ec2")
VPC_ID = "vpc-0c3ba38217caea010"  # Last vpc


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
    group_id = response.get("GroupId")

    print("Security Group Id - ", group_id)

    return group_id


def add_ssh_access_sg(sg_id, ip_address):
    ip_address = f"{ip_address}/32"

    response = ec2_client.authorize_security_group_ingress(
        CidrIp=ip_address,
        FromPort=22,
        GroupId=sg_id,
        IpProtocol='tcp',
        ToPort=22,
    )
    if response.get("Return"):
        print("Rule added successfully")
    else:
        print("Rule was not added")


def add_http_access_sg(sg_id):
    response = ec2_client.authorize_security_group_ingress(
        CidrIp="0.0.0.0/0",
        FromPort=80,
        GroupId=sg_id,
        IpProtocol='tcp',
        ToPort=80,
    )
    if response.get("Return"):
        print("Rule added successfully")
    else:
        print("Rule was not added")


def run_ec2(sg_id, subnet_id):
    response = ec2_client.run_instances(
        # in lab we don't have machines which has volumetype gp2
        # and instance typ t2.micro
        BlockDeviceMappings=[
            {
                "DeviceName": "/dev/sdh",
                "Ebs": {"DeleteOnTermination": True,
                        "VolumeSize": 10,
                        "VolumeType": "gp2",
                        "Encrypted": False},
            },
        ],
        ImageId="ami-0022f774911c1d690",
        InstanceType="t3.micro",
        KeyName="my-demo-key",
        MaxCount=1,
        MinCount=1,
        Monitoring={"Enabled": True},
        # SecurityGroupIds=[
        #     sg_id,
        # ],
        # SubnetId=subnet_id,
        UserData="""#!/bin/bash
       echo "Hello I am from user data" > info.txt
       """,
        InstanceInitiatedShutdownBehavior="stop",
        NetworkInterfaces=[
            {
                "AssociatePublicIpAddress": True,
                "DeleteOnTermination": True,
                "Groups": [
                    sg_id,
                ],
                "DeviceIndex": 0,
                "SubnetId": subnet_id,
            },
        ],
    )
    for instance in response.get("Instances"):
        instance_id = instance.get("InstanceId")
        print("InstanceId - ", instance_id)
    # pprint(response)

    return None


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP





def main():
    #sg_id = create_security_group("ec2-sg", "Security group to enable access on ec2")
    #print(sg_id)
    # add rule for all http
    #add_http_access_sg(sg_id)
    # attach ssh port to security group
    #add_ssh_access_sg(sg_id, extract_ip())
    #create_key_pair("my-demo-key")
    run_ec2("sg-011665d7e1b27dbaa", "subnet-062082d1e7add345c")


if __name__ == "__main__":
    main()
