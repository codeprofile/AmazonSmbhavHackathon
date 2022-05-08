import boto3

ACCESS_KEY = ''
SECRET_KEY = ''

dynamodb_client = boto3.client(
    'dynamodb',
    verify=False,
    region_name="ap-southeast-1",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)


table_name = 'artwork_data'
existing_tables = dynamodb_client.list_tables()
if table_name not in existing_tables:
    try:
        response = dynamodb_client.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N',
                },
                {
                    'AttributeName': 'artistName',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'artistDescription',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'artName',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'artDescription',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'artPrice',
                    'AttributeType': 'N',
                },
                {
                    'AttributeName': 'artLink',
                    'AttributeType': 'S',
                },
            ],
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH',
                },
                {
                    'AttributeName': 'artistName',
                    'KeyType': 'RANGE',
                },
                {
                    'AttributeName': 'artistDescription',
                    'KeyType': 'RANGE',
                },
                {
                    'AttributeName': 'artName',
                    'KeyType': 'HASH',
                },
                {
                    'AttributeName': 'artDescription',
                    'KeyType': 'RANGE',
                },
                {
                    'AttributeName': 'artPrice',
                    'KeyType': 'RANGE',
                },
                {
                    'AttributeName': 'artLink',
                    'KeyType': 'RANGE',
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10,
            },
            TableName=table_name,
        )
        print(response)
        # return True
    except Exception as e:
        print(e)


