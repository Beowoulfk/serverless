import json
import decimal
import boto3


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('usersTable')

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

def update_users(event, context):
    table_name = 'usersTable'
    user_id = event['pathParameters']['id']
    body = json.loads(event['body'])

    update_expression = 'set '
    expression_attribute_names = {}
    expression_attribute_values = {}

    for key, value in body.items():
        attribute_name = '#' + key
        attribute_value = ':' + key
        update_expression += f'{attribute_name} = {attribute_value}, '
        expression_attribute_names[attribute_name] = key
        expression_attribute_values[attribute_value] = value

    update_expression = update_expression[:-2]  # Eliminar la coma y el espacio extra al final

    params = {
        'TableName': table_name,
        'Key': {'pk': user_id},
        'UpdateExpression': update_expression,
        'ExpressionAttributeNames': expression_attribute_names,
        'ExpressionAttributeValues': expression_attribute_values,
        'ReturnValues': 'ALL_NEW'
    }

    response = table.update_item(**params)

    return {
        'statusCode': 200,
        'body': json.dumps({'user': response['Attributes']}, cls=DecimalEncoder)
    }