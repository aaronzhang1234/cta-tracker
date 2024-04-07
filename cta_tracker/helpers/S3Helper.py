import json

import boto3


class S3Helper:
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def add_json_to_s3(self, json_object, file_name):
        try:
            self.s3_client.put_object(
                Body=json.dumps(json_object),
                Bucket="cta-jsons",
                Key=file_name
            )
        except Exception as e:
            printf(f"Unable to add to S3 Bucket for item {file_name} and error {e}")
