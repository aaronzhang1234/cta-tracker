import boto3


class DynamoDBHelper:
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('cta_tracker')

    def add_to_dynamo(self, train_item):
        try:
            self.table.put_item(
                Item=train_item
            )
        except Exception as e:
            print(f"Failed to add Item to dynamo with partition key {train_item} with exception {e}")

    def get_item(self, primary_key):
        try:
            item = self.table.get_item(
                Key={
                    'train_identifier': primary_key
                }
            )
            if "Item" in item:
                return item["Item"]
        except Exception as e:
            printf(f"Failed to get item with primary key of {primary_key} with exception {e}")
            return None
