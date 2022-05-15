import boto3

ec2_client = boto3.client('ec2')


def create_vpc():
    response = ec2_client.create_vpc(CidrBlock="10.10.0.0/16")
    vpc_id = response.get('Vpc').get('VpcId')
    waiter = ec2_client.get_waiter("vpc_available")
    waiter.wait(
        VpcIds=[
            vpc_id
        ]
    )
    ec2_client.create_tags(
        Resources=[vpc_id],
        Tags=[{"Key": "Name", "Value": "firstVpc"},
              {"Key": "Creator", "Value": "Salome Tkhilaishvili"}]
    )

    return vpc_id


def create_subnet(vpc_id, cidr_block):
    response = ec2_client.create_subnet(VpcId=vpc_id, CidrBlock=cidr_block)
    subnet = response.get("Subnet")
    subnet_id = subnet.get("SubnetId")
    return subnet_id


def create_route_table_without_route(vpc_id):
    response = ec2_client.create_route_table(VpcId=vpc_id)
    route_table = response.get("RouteTable")
    route_table_id = route_table.get("RouteTableId")
    return route_table_id


def create_and_attach_igw(vpc_id):
    response = ec2_client.create_internet_gateway()
    igw = response.get("InternetGateway")
    igw_id = igw.get("InternetGatewayId")
    # attach gateway to vpc
    response = ec2_client.attach_internet_gateway(
        InternetGatewayId=igw_id,
        VpcId=vpc_id
    )
    return igw_id


def create_route_table_with_route(route_table_id, igw_id):
    response = ec2_client.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=igw_id,
        RouteTableId=route_table_id
    )


def attach_subnet_to_route(subnet_id, rtb_id):
    response = ec2_client.associate_route_table(
        RouteTableId=rtb_id,
        SubnetId=subnet_id
    )


def main():
    vpc_id = create_vpc()
    print(f'print vcp id {vpc_id}')
    subnet_id = create_subnet(vpc_id, "10.10.0.0/16")
    print(f'print subnet id {subnet_id}')
    igw_id = create_and_attach_igw(vpc_id)
    print(f'print internet gateway id {igw_id}')
    rtb_id = create_route_table_without_route(vpc_id)
    print(f'print router table id {rtb_id}')
    create_route_table_with_route(rtb_id, igw_id)
    attach_subnet_to_route(subnet_id, rtb_id)

    # create private subnet
    #private_subnet_id = create_subnet("vpc-0598d9d2ea79d8cea", "10.10.1.128/17")
    #print(f'print private subnet id {private_subnet_id}')
    #private_rtb_id = create_route_table_without_route("vpc-0598d9d2ea79d8cea")
    #print(f'print private route table id {private_rtb_id}')
    #attach_subnet_to_route(private_subnet_id, private_rtb_id)


if __name__ == "__main__":
    main()
