import boto3
import datetime
from botocore.config import Config
from botocore.exceptions import ClientError


class AWSService():
    def __init__(self):
        dict_conn = dict(line.strip().split('=') for line in open('connection.properties'))
        self.expiry = dict_conn["EXPIRY"]
        self.access_key = dict_conn["ACCESS_KEY"]
        self.secret_key = dict_conn["SECRET_KEY"]
        self.region_name = dict_conn["REGION_NAME"]
        self.bucket_name = dict_conn["BUCKET_NAME"]
        self.client = self.get_client()

    def get_client(self):
        session = boto3.session.Session()
        client = session.client(
            "s3", region_name=self.region_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config('us-east-1')
        )

        return client

    def create_presigned_url(self, object_key):
        try:
            timestamp = datetime.datetime.now()
            response = self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_key},
                ExpiresIn=self.expiry,
                HttpMethod="GET"
            )
            return response, timestamp
        except ClientError as e:
            print(e)
