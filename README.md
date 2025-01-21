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
| `return_loc`   | String (Optional) | If present, then returns current locations of trains |

### Response
```json
{
  "no_of_trains": (Number of Trains in Response),
  "stops" : (List of Stops for this route),
  "route" : (Route of this request),
  "stats": {
   "avg_total_time": (Average time of all trains),
   "avg_time_between_stops" : DICT (Average time between each stop, Key is stopid-stopid),
  },
  "trains": [
    {
      "route_number" : (CTA Train Number),
      "start_time" : (Time when train object was created),
      "stop_times" :  (Stop times, correspond to train_stop location, can be Null if not available),
      "total_time" : (Total time of the trip)
    }....
  ]
}

```
## Local Setup

Add helper_layer as a source folder on Pycharm. `Settings > Project Structure`

You need to configure the AWS profile for local development. Either create a new access-id/secret or reuse a previous one.


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