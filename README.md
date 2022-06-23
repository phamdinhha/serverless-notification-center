# Serverless websocket notification center
A serverless notification center using AWS Websocket API

![alt text](https://github.com/phamdinhha/serverless-notification-center/blob/main/imgs/noti-service.drawio.png)

## Installation
Make sure you have enough permissions on your AWS account to:
- Create IAM roles
- Create/list s3 buckets
- Create/write to/read from DynamoDB tables
- Create/execute lambda functions 
- Create/use lambda layers
- Create/list/write/read messages from SQS queues
- Create/send event from AWS Evenbridge

Make sure you have [AWS SAM](https://aws.amazon.com/serverless/sam/) installed on your workspace and run the following command:
```
sam deploy --guided
```

## Testing
Use postman to connect to your Websocket API.
Use AWS EvenBridge to send push notification to the clients

## AWS infrastructures
All AWS infrastructures for this project are defined in [template.yml](https://github.com/phamdinhha/serverless-notification-center/blob/main/template.yaml)


## Lamdas
### Authorizer
Handle authorization when client connect to the websocket API, you can write your own custom lambda authorizer
Custom authorizer have to return the policy document that specify the allowed actions on the specified resources
```
return {
    "principalId": claims["email"],
    "policyDocument": {
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "execute-api:Invoke",
            "Effect": "Allow",
            "Resource": event["methodArn"]
        }]
    },
    "context": {
        "userId": claims["email"]
    }
}
```
### Create socket connection
Handle the create connection request from clients. In this example I insert the user_id and connection_id to a DynamoDB table

### Delete socket connection
Handle the delete connection request from clients.

### Notify users
Handle event when the server want to send notification to a specific user.
