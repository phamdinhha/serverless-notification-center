import boto3
import os

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ["TABLE_NAME"]

def handler(event, context):
    try:
        connection_id = event['requestContext']['connectionId']
        print("connection id: ", connection_id)
        delete_all_connection(connection_id=connection_id)
        return {
            'statusCode': 200,
            'body': 'disconnected'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'failed to disconnect'
        }


def delete_all_connection(connection_id):
    try:
        table = dynamodb.Table(TABLE_NAME)
        print(connection_id)
        table.delete_item(
            Key={
                'pk': connection_id,
                'sk': "connection#"
            }
        )
    except Exception as e:
        print(e)
        raise e
