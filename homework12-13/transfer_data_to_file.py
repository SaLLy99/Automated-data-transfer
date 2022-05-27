import boto3

dynamodb = boto3.resource('dynamodb')


def transfer_data_to_file(table_name):
    client = boto3.client('dynamodb')

    response = client.describe_table(
        TableName=table_name
    )
    item_array = response.get('Table').get('AttributeDefinitions')
    key_array = []
    for item in item_array:
        key_array.append(item.get('AttributeName'))

    table = dynamodb.Table(table_name)
    response = table.scan()
    data = response['Items']
    with open("dynamo.txt", "a") as file:
        for item in data:
            for key in key_array:
                print(item.get(key))
                file.write(item.get(key)+"\n")


def main():
    transfer_data_to_file("Employees")


if __name__ == "__main__":
    main()
