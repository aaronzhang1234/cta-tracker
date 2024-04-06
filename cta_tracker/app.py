import json
import requests
import boto3

from helpers.DynamoDBHelper import DynamoDBHelper
from helpers.CTAHelper import CTAHelper

def lambda_handler(event, context):
    dynamo_helper = DynamoDBHelper()
    cta_helper = CTAHelper()
    try:
        routes = cta_helper.get_locations_response()
        for route in routes:
            route_name = route["@name"]
            if "train" not in route:
                print(f"No trains for {route_name}")
                continue
            trains = route["train"]
            for train in trains:
                primary_key = cta_helper.get_train_id(route_name, train)
                train_item = dynamo_helper.get_item(primary_key)
                if train_item:
                    train_schedule = train_item["train_schedule"]
                    nextStaId, arrivalTime = cta_helper.get_next_train_station(train)
                    if not (nextStaId in train_schedule and train_schedule[nextStaId] == arrivalTime):
                        train_schedule[nextStaId] = arrivalTime
                        dynamo_helper.add_to_dynamo(train_item)
                    else:
                        print("Same as usual")
                else:
                    train_item = cta_helper.create_train_item(primary_key, route_name, train)
                    dynamo_helper.add_to_dynamo(train_item)

    except requests.RequestException as e:
        raise e
    return {
       "statusCode": 200
    }

if __name__=="__main__":
    print(lambda_handler(event={}, context=None))