import datetime

from dynamo_helper import DynamoHelper
from cta_helper import CTAHelper
from s3_helper import S3Helper
import pandas as pd
import json
from panda_functions import pandas_fun, timedelta_to_string

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False

def lambda_handler(event, context):
    logger.debug(event["headers"])
    try:
        if "return_loc" in event["headers"]:
            s3_helper = S3Helper()
            response = s3_helper.get_file("current_locs.json")
        else:
            response = json.dumps(get_stops_response(event))
        return {
            "body": response,
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type, start_time, end_time, route, show_trains',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            "statusCode": 200}
    except Exception as e:
        logger.exception("Error in Lambda Execution")
        return {
            "body": str(e),
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type, start_time, end_time, route, show_trains',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            "statusCode": 500}


def get_stops_response(event):
    dynamo_helper = DynamoHelper()
    cta_helper = CTAHelper()

    color_rt = event["headers"]["route"]
    show_trains = event["headers"]["show_trains"]
    start_time = event["headers"]["start_time"]

    # TODO make end time optional
    end_time = event["headers"]["end_time"]


    items = dynamo_helper.get_items_date(color_rt, start_time, end_time)

    stop_ids = cta_helper.get_route_order(color_rt)
    stop_ids.insert(0, "Created Time")
    response = {"no_of_trains": len(items), "route": color_rt}
    train_items = []

    df = pd.DataFrame(columns=stop_ids)
    for item in items:
        train_item = {"route_number": item["route_number"], "start_time": item["created_timestamp"], "uuid":item["train_uuid"]}

        sched = item["train_schedule"]
        stop_list = get_schedule_with_missing(sched, stop_ids, item["created_timestamp"])

        # We are returning this in lists because lists keep their order. Dicts do not.
        train_item["stop_times"] = stop_list
        train_item["total_time"] = None

        if stop_list[-1]:
            time_between = convert_to_date_obj(stop_list[-1]) - convert_to_date_obj(stop_list[0])
            train_item["total_time"] = timedelta_to_string(time_between)

        train_items.append(train_item)
        try:
            df.loc[item["train_uuid"]] = stop_list
        except Exception as e:
            logger.debug("item is", item)
            logger.debug("# of stops is", len(stop_ids))
            logger.debug("stop list is", stop_list)
            raise Exception(e)

    response["stats"] = pandas_fun(df)

    if show_trains:
        response["trains"] = train_items

    return response


def get_schedule_with_missing(schedule, color_order, created_time):
    stop_time_list = [created_time]
    for stop in color_order:
        if stop == "Created Time":
            continue
        if stop in schedule:
            stop_time_list.append(schedule[stop])
        else:
            stop_time_list.append(None)
    return stop_time_list

def convert_to_date_obj(date_str):
    no_micro = date_str.split(".")[0]
    return datetime.datetime.strptime(no_micro, "%Y-%m-%dT%H:%M:%S")

if __name__ == "__main__":
    f = open('event.json')
    event_json = json.load(f)
    print(lambda_handler(event=event_json, context=None))
