import boto3

ec2_client = boto3.client('ec2')


def create_vpc():
    response = ec2_client.create_vpc(CidrBlock="10.23.0.0/16")
    vpc_id = response.get("Vpc").get("VpcId")
    waiter = ec2_client.get_waiter("vpc_available")
    waiter.wait(
        VpcIds=[
            vpc_id
        ]
    )

    ec2_client.create_tags(
        Resources=[vpc_id],
        Tags=[{"Key": "Name", "Value": "firstVpc"}]
    )
    return vpc_id


def create_and_attach_igw(vpc_id):
    response = ec2_client.create_internet_gateway()
    print(response)
    igw = response.get("InternetGateway")
    igw_id = igw.get("InternetGatewayId")
    ec2_client.create_tags(
        Resources=[igw_id],
        Tags=[{"Key": "Name", "Value": "firstVpcIGW"}]
    )
    # attach gateway to vpc
    response = ec2_client.attach_internet_gateway(
        InternetGatewayId=igw_id,
        VpcId=vpc_id
    )
    print("attached")
    print(response)
    return igw_id


def main():
    vpc_id = create_vpc()
    igw_id = create_and_attach_igw(vpc_id)
    print(igw_id)


if __name__ == "__main__":
    main()
