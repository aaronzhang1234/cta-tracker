import datetime

from dateutil.parser import parse
from collections import OrderedDict
from dynamo_helper import DynamoHelper
from cta_helper import CTAHelper
import json

def lambda_handler(event, context):
    dynamo_helper = DynamoHelper()
    cta_helper = CTAHelper()
    print(event)

    color_rt = event["headers"]["route"]
    start_time = event["headers"]["start_time"]
    #TODO make end time optional poop
    end_time = event["headers"]["end_time"]
    items = dynamo_helper.get_items_date(color_rt, start_time, end_time)

    response = {"no_of_trains": len(items)}
    trains_item = []
    for item in items:
        train_item = {"route_number": item["route_number"], "start_time": item["created_timestamp"]}

        sched = item["train_schedule"]
        stops = get_schedule_with_missing(sched, cta_helper.get_route_order(color_rt))

        #We are returning this in lists because lists keep their order. Dicts do not.
        train_item["train_stops"] = list(stops.keys())
        train_item["stop_times"] = list(stops.values())
        trains_item.append(train_item)
    response["trains"] = trains_item
    return {
        "body": json.dumps(response),
        "headers": {
            'Access-Control-Allow-Headers': 'Content-Type, start_time, end_time, route',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "statusCode": 200}

def get_schedule_with_missing(schedule, color_order):
    stop_time_dict = {}
    for stop in color_order:
        if stop in schedule:
            stop_time_dict[stop] = schedule[stop]
        else:
            stop_time_dict[stop] = None
    return stop_time_dict

#TODO Do we need this method/ how to get station dict without calling it directly.
#def get_times_between(stops):
#        first_stop = list(stops.keys())[0]
#        last_stop = list(stops.keys())[len(stops.keys())-1]
#        first = convert_to_date_obj(stops[first_stop])
#        second = convert_to_date_obj(stops[last_stop])
#        total_time = second - first
#        return f"The Total between {station_dict.get(first_stop)} and {station_dict.get(last_stop)} is {total_time}"

def convert_to_date_obj(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

if __name__=="__main__":
    f = open('event.json')
    event_json = json.load(f)
    print(lambda_handler(event=event_json ,context=None))
    