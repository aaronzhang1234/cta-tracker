import boto3
from stations import station_dict
from dateutil.parser import parse
from collections import OrderedDict

def lambda_handler(event, context):
    route_json = { "40120" :  "2024-04-07T17:01:19" , "40310" :  "2024-04-07T16:57:14" , "40960" :  "2024-04-07T16:52:19" , "41060" :  "2024-04-07T17:03:16" , "41130" :  "2024-04-07T17:05:10" , "41150" :  "2024-04-07T16:55:17" , "41400" :  "2024-04-07T17:09:04" }
    try:
        wut = OrderedDict(sorted(route_json.items(), key=lambda x: parse(x[1])))
        for key in wut:
            value = route_json[key]
            name = station_dict.get(key)
            print(f"{name} , {value}")
    except Exception as e:
        raise e
    return {
       "statusCode": 200}
   
    

if __name__=="__main__":
    print(lambda_handler(event={} ,context=None))
    