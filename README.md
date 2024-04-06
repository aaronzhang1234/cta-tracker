# cta-tracker

Scheduled lambda that runs every 1 minute to get CTA data.

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