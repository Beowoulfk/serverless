import json
import uuid
import boto3


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('usersTable')

def create_users(event, context):
    table_name = 'usersTable'
    id = str(uuid.uuid4())
    user_body = json.loads(event['body'])
    
    user_body['pk'] = id
    
    
    params = {
        'TableName': table_name,
        'Item': user_body
    }
    
    table.put_item(Item=user_body)
    
    response = {
        'statusCode': 200,
        'body': json.dumps({'user': user_body})
    }
    
    return response