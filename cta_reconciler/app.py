import datetime

from stations import station_dict, station_order
from dateutil.parser import parse
from collections import OrderedDict
from helper_layer.DynamoDBHelper import DynamoDBHelper

def lambda_handler(event, context):
    color_rt = "brn-1"
    dynamo_helper = DynamoDBHelper()
    one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()
    items = dynamo_helper.get_items_date(color_rt, one_day_ago)
    color_order = station_order[color_rt]
    for item in items:
        sched = item["train_schedule"]
        wut = OrderedDict(sorted(sched.items(), key=lambda x: parse(x[1])))
        print(list(wut.keys()))
        if len(sched) == len(color_order):
            getTimesBetween(color_order, sched)
        else:
            diff = set(color_order) - set(sched.keys())
            for station in diff:
                print(station_dict[station], end="|")
            print("")

    wut = OrderedDict(sorted(items[6]["train_schedule"].items(), key=lambda x: parse(x[1])))
    for key in wut:
        value = items[1]["train_schedule"][key]
        name = station_dict.get(key)
        print(f"{name} , {value}")

    return {
       "statusCode": 200}

def getTimesBetween(ordered, item):
    first = convert_to_date_obj(item[ordered[0]])
    second = convert_to_date_obj(item[ordered[len(ordered)-1]])
    total_time = second - first
    print(f"The Total between {station_dict.get(ordered[0])} and {station_dict.get(ordered[len(ordered)-1])} is {total_time}")

def convert_to_date_obj(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

if __name__=="__main__":
    print(lambda_handler(event={} ,context=None))
    