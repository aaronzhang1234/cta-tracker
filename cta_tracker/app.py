import requests

from cta_helper import CTAHelper
from dynamo_helper import DynamoHelper
from s3_helper import S3Helper
import datetime


def lambda_handler(event, context):
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime("%Y-%m-%d")
    dynamo_helper = DynamoHelper()
    s3_helper = S3Helper()
    cta_helper = CTAHelper()
    try:
        cta_json = cta_helper.get_locations_response()
        file_name = current_datetime.isoformat() + ".json"
        s3_helper.add_json_to_s3(cta_json, file_name)
        routes = cta_json["ctatt"]["route"]
        for route in routes:
            route_name = route["@name"]
            if route_name != "red":
                continue
            if "train" not in route:
                print(f"No trains for {route_name}")
                continue
            trains = route["train"] if isinstance(route["train"], list) else [
                route["train"]]  #Sometimes the API will return back a single train object not in a list
            mins_ago = (datetime.datetime.now() - datetime.timedelta(minutes=5)).isoformat()
            combined_trains = (dynamo_helper.get_items_date(route_name + "-1", mins_ago) +
                               dynamo_helper.get_items_date(route_name + "-5", mins_ago))
            for train in trains:
                try:
                    updatable_object = get_updatable_object(train, combined_trains)
                    if updatable_object:
                        next_sta_id, arr_time = cta_helper.get_next_train_station(train)
                        updated_object = update_schedule(updatable_object, next_sta_id, arr_time)
                        dynamo_helper.add_to_dynamo(updated_object)
                        print(f"Updated! {updated_object['route_number']}-{updated_object['direction_code']}")
                    else:
                        primary_key, hash_key = cta_helper.get_train_id(route_name, train)
                        train_item = cta_helper.create_train_item(primary_key, hash_key, route_name, train)
                        dynamo_helper.add_to_dynamo(train_item)
                        print(f"Added! {train_item['route_number']}-{train_item['direction_code']}")
                except Exception as e:
                    print(f"Error parsing train with information {train}, error is {e}")
                    continue

    except requests.RequestException as e:
        raise e
    return {
        "statusCode": 200
    }


def get_updatable_object(train_item, dynamo_items):
    for dynamo_item in dynamo_items:
        if (dynamo_item["route_number"] == train_item["rn"] and
                dynamo_item["direction_code"] == train_item["trDr"]):
            return dynamo_item
    return None


def update_schedule(train_item, next_sta_id, arrival_time):
    train_schedule = train_item["train_schedule"]
    if not (next_sta_id in train_schedule and train_schedule[next_sta_id] == arrival_time):
        train_schedule[next_sta_id] = arrival_time
        train_item["last_updated_date"] = datetime.datetime.now().isoformat()
        return train_item


if __name__ == "__main__":
    print(lambda_handler(event={}, context=None))
