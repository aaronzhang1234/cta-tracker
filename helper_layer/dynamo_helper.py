import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime

class DynamoHelper:
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('cta_tracker')

    def add_to_dynamo(self, train_item):
        try:
            self.table.put_item(
                Item=train_item
            )
        except Exception as e:
            raise Exception(f"Failed to add Item to dynamo with partition key {train_item} with exception {e}")

    def get_items_date(self, primary_key, start_time=None, end_time=None):
        if end_time is None:
            end_time = datetime.now().isoformat()
        try:
            item = self.table.query(
                IndexName="updated_date_lsi",
                KeyConditionExpression=Key('train_identifier').eq(primary_key) &
                                       Key('last_updated_date').between(start_time, end_time)
            )
            if "Items" in item:
                return item["Items"]
        except Exception as e:
            raise Exception(f"Failed to get item with primary key of {primary_key} with exception {e}")
            return None
