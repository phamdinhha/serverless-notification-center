import boto3
import os

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ["TABLE_NAME"]

def handler(event, lambda_context):
    print("event: ", event)
    print("lambda context: ", lambda_context)
    try:
        save_connection(event['requestContext'])
        return {
            'statusCode': 200,
            'headers': {
                'Sec-WebSocket-Protocol': 'websocket'
            },
            'body': 'connected to websocket api'
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': 'connected to websocket api'
        }
        

def save_connection(request_context):
    try:
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(
            Item={
                'pk': request_context['connectionId'],
                'sk': "connection#",
                'ipAddress': request_context['identity']['sourceIp'],
                'connectedAt': request_context['connectedAt'],
                'ttl': get_time_to_live(),
                'UserID': request_context['authorizer']['userId'],
                'UserSK': 'user#'
            }
        )
    except Exception as e:
        raise e

def get_time_to_live():
    return int(24*60*60)