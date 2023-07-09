import boto3
import json
import decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('usersTable')


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

def get_users(event, context):
    item_id = event['pathParameters']['id']
    response = table.get_item(Key={'pk': item_id})
    item = response.get('Item')
    if item:
        response = {
            'statusCode': 200,
            'body': json.dumps(item, cls=DecimalEncoder)
        }
    else:
        response = {
            'statusCode': 404,
            'body': json.dumps({'message': 'Item not found'})
        }

    return response

