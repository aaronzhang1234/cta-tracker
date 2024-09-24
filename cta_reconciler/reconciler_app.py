import datetime

from dateutil.parser import parse
from collections import OrderedDict
from dynamo_helper import DynamoHelper
from cta_helper import CTAHelper
from s3_helper import S3Helper
import pandas as pd
import json

fake_dynamo = [{'last_updated_epoch': '1720931009', 'train_date': '2024-07-13', 'last_updated_date': '2024-07-14T00:11:29.825030', 'train_schedule': {'40680': '2024-07-13T23:31:16', '40460': '2024-07-13T23:36:41', '41010': '2024-07-14T00:07:35', '40360': '2024-07-13T23:58:01', '40040': '2024-07-13T23:27:14', '40260': '2024-07-13T23:34:13', '41310': '2024-07-13T23:59:18', '40660': '2024-07-13T23:46:10', '41210': '2024-07-13T23:51:42', '40800': '2024-07-13T23:42:16', '40160': '2024-07-13T23:28:13', '40380': '2024-07-13T23:35:14', '41290': '2024-07-14T00:12:01', '41220': '2024-07-13T23:48:03', '41440': '2024-07-14T00:00:07', '41460': '2024-07-14T00:01:19', '40850': '2024-07-13T23:29:08', '40530': '2024-07-13T23:51:02', '40870': '2024-07-14T00:10:11', '41320': '2024-07-13T23:55:19', '41700': '2024-07-13T23:31:56', '40710': '2024-07-13T23:38:47', '40730': '2024-07-13T23:25:13', '41500': '2024-07-14T00:03:36', '40090': '2024-07-14T00:05:22', '41480': '2024-07-14T00:07:10', '41180': '2024-07-14T00:11:14'}, 'direction_code': '1', 'delayed': '0', 'created_timestamp': '2024-07-13T23:23:29.936866', 'route_number': '418', 'train_identifier': 'brn-1', 'route_name': 'brn', 'train_uuid': 'd2a077c5-a978-4261-93f7-1275ae1cdd7d'}, {'last_updated_epoch': '1720932030', 'train_date': '2024-07-13', 'last_updated_date': '2024-07-14T00:28:29.625724', 'train_schedule': {'40680': '2024-07-13T23:51:18', '40460': '2024-07-13T23:56:07', '41010': '2024-07-14T00:24:52', '40360': '2024-07-14T00:15:18', '40040': '2024-07-13T23:42:53', '40260': '2024-07-13T23:53:13', '41310': '2024-07-14T00:16:37', '40660': '2024-07-14T00:05:12', '41210': '2024-07-14T00:11:19', '40800': '2024-07-14T00:02:18', '40160': '2024-07-13T23:45:10', '40380': '2024-07-13T23:54:02', '41290': '2024-07-14T00:28:56', '41220': '2024-07-14T00:08:03', '41440': '2024-07-14T00:18:11', '41460': '2024-07-14T00:18:34', '40530': '2024-07-14T00:09:58', '40870': '2024-07-14T00:27:15', '41320': '2024-07-14T00:13:01', '40710': '2024-07-13T23:58:16', '40730': '2024-07-13T23:42:19', '41500': '2024-07-14T00:20:52', '40090': '2024-07-14T00:23:13', '41480': '2024-07-14T00:23:33', '41180': '2024-07-14T00:28:12'}, 'direction_code': '1', 'delayed': '0', 'created_timestamp': '2024-07-13T23:40:30.178814', 'route_number': '419', 'train_identifier': 'brn-1', 'route_name': 'brn', 'train_uuid': '51bb5dee-ed2e-4297-aaca-578ff9cf589d'}, {'last_updated_epoch': '1720932449', 'train_date': '2024-07-13', 'last_updated_date': '2024-07-14T00:33:29.646473', 'train_schedule': {'40680': '2024-07-13T23:55:18', '40460': '2024-07-14T00:00:12', '41010': '2024-07-14T00:29:39', '40040': '2024-07-13T23:50:13', '40260': '2024-07-13T23:57:14', '41310': '2024-07-14T00:21:07', '40660': '2024-07-14T00:10:15', '41210': '2024-07-14T00:14:59', '40800': '2024-07-14T00:06:11', '40160': '2024-07-13T23:52:12', '40380': '2024-07-13T23:58:01', '41290': '2024-07-14T00:33:51', '41220': '2024-07-14T00:11:17', '41440': '2024-07-14T00:21:56', '41460': '2024-07-14T00:24:19', '40850': '2024-07-13T23:52:52', '40530': '2024-07-14T00:14:05', '40870': '2024-07-14T00:32:01', '41320': '2024-07-14T00:17:10', '40710': '2024-07-14T00:02:01', '40730': '2024-07-13T23:49:19', '41500': '2024-07-14T00:25:42', '40090': '2024-07-14T00:28:10', '41480': '2024-07-14T00:29:15', '41180': '2024-07-14T00:33:19'}, 'direction_code': '1', 'delayed': '0', 'created_timestamp': '2024-07-13T23:47:29.644573', 'route_number': '414', 'train_identifier': 'brn-1', 'route_name': 'brn', 'train_uuid': '11d951a7-8ff8-4a57-9159-b387e8453e5d'}, {'last_updated_epoch': '1720932989', 'train_date': '2024-07-13', 'last_updated_date': '2024-07-14T00:42:29.766328', 'train_schedule': {'40680': '2024-07-14T00:04:12', '40460': '2024-07-14T00:09:14', '41010': '2024-07-14T00:38:45', '40360': '2024-07-14T00:29:11', '40040': '2024-07-14T00:00:11', '40260': '2024-07-14T00:07:09', '41310': '2024-07-14T00:30:47', '40660': '2024-07-14T00:19:17', '41210': '2024-07-14T00:25:17', '40800': '2024-07-14T00:15:12', '40160': '2024-07-14T00:02:11', '41290': '2024-07-14T00:43:03', '41220': '2024-07-14T00:21:16', '41440': '2024-07-14T00:31:59', '41460': '2024-07-14T00:33:23', '40530': '2024-07-14T00:23:58', '40870': '2024-07-14T00:41:09', '41320': '2024-07-14T00:26:20', '41700': '2024-07-14T00:05:00', '40710': '2024-07-14T00:12:19', '40730': '2024-07-13T23:58:19', '41500': '2024-07-14T00:34:54', '40090': '2024-07-14T00:37:01', '41480': '2024-07-14T00:38:12', '41180': '2024-07-14T00:42:12'}, 'direction_code': '1', 'delayed': '0', 'created_timestamp': '2024-07-13T23:56:29.948817', 'route_number': '420', 'train_identifier': 'brn-1', 'route_name': 'brn', 'train_uuid': 'b7314ac0-9e16-4d72-9f26-a287b09a7393'}, {'last_updated_epoch': '1720933949', 'train_date': '2024-07-14', 'last_updated_date': '2024-07-14T00:58:29.487095', 'train_schedule': {'40680': '2024-07-14T00:19:30', '40460': '2024-07-14T00:26:13', '41010': '2024-07-14T00:55:14', '40360': '2024-07-14T00:45:03', '40040': '2024-07-14T00:14:56', '40260': '2024-07-14T00:24:19', '41310': '2024-07-14T00:47:00', '40660': '2024-07-14T00:35:14', '41210': '2024-07-14T00:40:31', '40800': '2024-07-14T00:32:16', '40160': '2024-07-14T00:16:14', '40380': '2024-07-14T00:25:17', '41290': '2024-07-14T00:59:10', '41220': '2024-07-14T00:37:16', '41440': '2024-07-14T00:48:06', '41460': '2024-07-14T00:49:29', '40850': '2024-07-14T00:16:58', '40530': '2024-07-14T00:38:52', '40870': '2024-07-14T00:56:16', '41320': '2024-07-14T00:42:54', '41700': '2024-07-14T00:22:07', '40710': '2024-07-14T00:28:06', '40730': '2024-07-14T00:14:18', '41500': '2024-07-14T00:50:47', '40090': '2024-07-14T00:52:33', '41480': '2024-07-14T00:54:03', '41180': '2024-07-14T00:58:04'}, 'direction_code': '1', 'delayed': '0', 'created_timestamp': '2024-07-14T00:12:29.805048', 'route_number': '421', 'train_identifier': 'brn-1', 'route_name': 'brn', 'train_uuid': '4b24b410-0df8-43e3-914c-78d83b2358eb'}]

def lambda_handler(event, context):
    try:
        if "return_loc" in event["headers"]:
            s3_helper = S3Helper()
            response = s3_helper.get_file("current_locs.json")
        else:
            response = json.dumps(get_stops_response(event))
        return {
            "body": response,
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type, start_time, end_time, route',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            "statusCode": 200}
    except Exception as e:
        return {
            "body": str(e),
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type, start_time, end_time, route',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            "statusCode": 500}



def get_stops_response(event):
    dynamo_helper = DynamoHelper()
    cta_helper = CTAHelper()
    color_rt = event["headers"]["route"]
    start_time = event["headers"]["start_time"]
    # TODO make end time optional
    end_time = event["headers"]["end_time"]
    items = fake_dynamo #dynamo_helper.get_items_date(color_rt, start_time, end_time)
    stop_ids = cta_helper.get_route_order(color_rt)
    response = {"no_of_trains": len(items), "stops": stop_ids, "route": color_rt}
    train_items = []

    df = pd.DataFrame(columns= stop_ids)
    for item in items:
        train_item = {"route_number": item["route_number"], "start_time": item["created_timestamp"]}

        sched = item["train_schedule"]
        stop_list = get_schedule_with_missing(sched, stop_ids)

        # We are returning this in lists because lists keep their order. Dicts do not.
        train_item["stop_times"] = stop_list
        train_item["total_time"] = None

        if stop_list[-1]:
            total_time = int((convert_to_date_obj(stop_list[-1]) - convert_to_date_obj(item["created_timestamp"])).total_seconds())
            hours, remainder = divmod(total_time, 60*60)
            minutes, seconds = divmod(remainder, 60)
            train_item["total_time"] = f"{hours}:{minutes}:{seconds}"

        train_items.append(train_item)

        df.loc[item["route_number"]] = stop_list
    response["stats"] = pandas_fun(df)
    response["trains"] = train_items
    return response


def get_schedule_with_missing(schedule, color_order):
    stop_time_list = []
    for stop in color_order:
        if stop in schedule:
            stop_time_list.append(schedule[stop])
        else:
            stop_time_list.append(None)
    return stop_time_list

def pandas_fun(df):
    #TODO Fill response with avg stats.
    for column in df:
        df[column] = pd.to_datetime(df[column], format="ISO8601")
    times_between = pd.DataFrame()
    columns = df.columns.values
    for idx in range(len(columns)-1):
        times_between_stops = df[columns[idx+1]] - df[columns[idx]]
        column_name = f"{columns[idx]} - {columns[idx+1]}"
        times_between[column_name] = times_between_stops
    print(times_between.sum())
    print(times_between.mean())


def convert_to_date_obj(date_str):
    no_micro = date_str.split(".")[0]
    return datetime.datetime.strptime(no_micro, "%Y-%m-%dT%H:%M:%S")


if __name__ == "__main__":
    f = open('event.json')
    event_json = json.load(f)
    print(lambda_handler(event=event_json, context=None))
