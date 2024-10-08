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
  "trains": [
    {
      "route_number" : (CTA Train Number),
      "start_time" : (Time when train object was created),
      "train_stops" : (List of Stops for this train),
      "stop_times" :  (Stop times, correspond to train_stop location, can be Null if not available) 
    }....
  ]
}

```

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