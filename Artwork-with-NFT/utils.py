import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = ''
SECRET_KEY = ''


def upload_to_aws(local_file, bucket, s3_file):
    s3_client = boto3.client(
        "s3",
        endpoint_url="https://s3.amazonaws.com",
        verify=False,
        region_name=None,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )

    try:
        s3_client.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def insert_data_db(tablename:str,data:dict):
    dynamodb = boto3.resource(
        'dynamodb',
        verify=False,
        region_name="ap-southeast-1",
        aws_access_key_id= ACCESS_KEY,
        aws_secret_access_key = SECRET_KEY,
    )
    try:
        # db_table = dynamodb.Table(tablename)
        dynamodb.Table(tablename).put_item(Item=data)
        print("Successfully inserted")
        return True
    except Exception as e:
        print(e)
        print("Failure")
        return False


def scanRecursive(tableName, **kwargs):
    """
    NOTE: Anytime you are filtering by a specific equivalency attribute such as id, name
    or date equal to ... etc., you should consider using a query not scan

    kwargs are any parameters you want to pass to the scan operation
    """
    dynamodb = boto3.resource(
        'dynamodb',
        verify=False,
        region_name="ap-southeast-1",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    dbTable = dynamodb.Table(tableName)
    response = dbTable.scan(**kwargs)
    if kwargs.get('Select') == "COUNT":
        return response.get('Count')
    data = response.get('Items')
    while 'LastEvaluatedKey' in response:
        response = kwargs.get('table').scan(ExclusiveStartKey=response['LastEvaluatedKey'], **kwargs)
        data.extend(response['Items'])
    return data

if __name__ == "__main__":
    # uploaded = upload_to_aws('C:\\Users\\HC117BC\\Downloads\\Amazon_Smbhav\\luma-ticket.png', 'nftmetadata1', 'digital_Asset')
    # data = {"id":1,"artist_name":"Laxmi Sarki","artist_description":"Best artist we can ever get","art_name":"Hopes","art_description":"lots of hopes","art_price":100000000}
    # insert_data_db("artworkdata",data)
    print(scanRecursive("artworkdata"))