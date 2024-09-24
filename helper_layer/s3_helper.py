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

            self.s3_client.put_object(
                Body=json.dumps(json_object),
                Bucket="cta-jsons",
                Key="current_locs.json"
            )
        except Exception as e:
            print(f"Unable to add to S3 Bucket for item {file_name} and error {e}")
    def get_file(self, file_name):
        try:
            s3_object = self.s3_client.get_object(
                Bucket="cta-jsons",
                Key=file_name
            )
            return s3_object["Body"].read().decode()
        except Exception as e:
            print(f"Unable to add to S3 Bucket for item {file_name} and error {e}")


