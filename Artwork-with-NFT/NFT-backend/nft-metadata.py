import boto3
import botocore
import json

BUCKET_NAME = 'my-bucket'

s3 = boto3.resource(service_name='s3',
                    region_name="ap-southeast-1",
                    aws_access_key_id="",
                    aws_secret_access_key=""
                    )

bucket = s3.Bucket('nftmetadata1')
dest_bucket = s3.Bucket('nftmetadata2')


try:
    for obj in bucket.objects.all():
        key = obj.key
        body = obj.get()['Body'].read()

        BASE_JSON = {
            "name": key,
            "description": "This is NFT collection"
        }
        s3.Object('nftmetadata2', f'{key}.json').put(Body=(json.dumps(BASE_JSON)))
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise
