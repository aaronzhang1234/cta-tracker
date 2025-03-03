# cta-tracker

Scheduled lambda that runs every 1 minute to get CTA data.

## Tracker

## Reconciler

### Request
| Request Header | Type              | Description                                          |
|----------------|-------------------|------------------------------------------------------|
| `start_time`   | String (ISO)      | Start time on when to search for trains              |
| `end_time`     | String (ISO)      | End time on when to search for trains                |
| `route`        | String            | Train to search for                                  |
| `show_trains`  | String            | If true, then returns every trains time.             |
| `return_loc`   | String (Optional) | If present, then returns current locations of trains |

### Response
```json
{
  "no_of_trains": (Number of Trains in Response),
  "route" : (Route of this request),
  "full_route_stats": {
   "avg_total_time": (Average time of all trains),
   "slowest_train":{
     "total_time" : (Total time of slowest train),
     "train_uuid": (UUID of train with slowest time) 
   }, 
   "fastest_train":{
     "total_time" : (Total time of fastest train),
     "train_uuid": (UUID of train with fastest time)
   }
  },
  "time_between_stats": {
    (Keys will be stopid-stopid):{
      "max_time": (Maximum amount of time it took for leg),
      "max_time_uuid": (UUID of train with max time),
      "mean_time": (Mean time of leg)
    }
  },
  "trains": [
    {
      "route_number" : (CTA Train Number),
      "start_time" : (Time when train object was created),
      "uuid": (Train UUID),
      "stop_times" :  (Stop times, correspond to train_stop location, can be Null if not available),
      "total_time" : (Total time of the trip)
    }....
  ]
}

```
## Local Setup

Add helper_layer as a source folder on Pycharm. `Settings > Project Structure`

You need to configure the AWS profile for local development. Either create a new access-id/secret or reuse a previous one.

This application uses local Dynamo to speed local development. [Deets in the link](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html)

## SAM i am

```bash
sam build
sam deploy --guided
```
```bash
sam local invoke 
```
```bash
sam delete --stack-name "cta-tracker"
```

## Resources

[AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)

[Scheduled Event](https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#schedule)

[CTA API]("https://www.transitchicago.com/developers/ttdocs/")