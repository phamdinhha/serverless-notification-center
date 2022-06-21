import boto3
from boto3.dynamodb.conditions import Key
import os
import json

dynamodb = boto3.resource('dynamodb')
apigateway_client = boto3.client('apigatewaymanagementapi', endpoint_url=os.environ["ENDPOINT"])
TABLE_NAME = os.environ["TABLE_NAME"]

def handler(event, context):
    print(event)
    try:
        records = event['Records']
        record_body = {}
        for record in records:
            if 'body' in record.keys():
                record_body = json.loads(record['body'])
        message_detail = record_body['detail']
        print("message detail: ", message_detail)
        user_id = message_detail['user_id']
        print("user_id: ", user_id)
        items = get_user_connections(user_id)
        send_notification_to_user(
            items, 
            message_detail['message'], 
            message_detail['callback']
        )
        return {
            'statusCode': 200,
            'body': 'successfully pushed to user'
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': 'failed to pushed to user'
        }

def send_notification_to_user(connections, message, callback):
    try:
        for connection in connections:
            data = {
                'type': "User Push Notification",
                'message': message,
                'callback': callback
            }
            print("post to connection: ", connection['pk'])
            apigateway_client.post_to_connection(
                Data=json.dumps(data).encode('utf-8'),
                ConnectionId=connection['pk']
            )
    except Exception as e:
        raise e

def get_user_connections(user_id):
    try:
        print("table_name: ", TABLE_NAME)
        table = dynamodb.Table(TABLE_NAME)
        response = table.query(
            IndexName='UserID',
            KeyConditionExpression=Key('UserID').eq(user_id)
        )
        print("Dynamo resposne: ", response)
        items = response['Items']
        print(items)
        return items
    except Exception as e:
        raise e

