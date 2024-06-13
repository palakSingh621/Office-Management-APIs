import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
office_table = dynamodb.Table('office_data')
transaction_table = dynamodb.Table('office_transactions')

status_check_path = '/status'
office_path = '/office'
offices_path = '/offices'
office_transaction_path = '/offices/transactions'

def lambda_handler(event, context):
    print('Request event: ', json.dumps(event))
    response = None

    try:
        http_method = event.get('httpMethod')
        path = event.get('path')

        if http_method == 'GET' and path == status_check_path:
            response = build_response(200, 'Service is operational')
        elif http_method == 'GET' and path == office_path:
            office_id = event['queryStringParameters']['id']
            response = get_office(office_id)
        elif http_method == 'GET' and path == offices_path:
            response = get_offices()
        elif http_method == 'POST' and path == office_path:
            response = save_office(json.loads(event['body']))
        elif http_method == 'PATCH' and path == office_path:
            body = json.loads(event['body'])
            response = modify_office(body['id'], body['updateKey'], body['updateValue'])
        elif http_method == 'DELETE' and path == office_path:
            body = json.loads(event['body'])
            response = delete_office(body['id'])
        elif http_method == 'POST' and path == office_transaction_path:
            response = create_office_transaction(json.loads(event['body']))
        else:
            response = build_response(404, '404 Not Found')

    except Exception as e:
        print('Error:', str(e))
        response = build_response(400, 'Error processing request')

    return response

def get_office(office_id):
    try:
        response = office_table.get_item(Key={'id': office_id})
        if 'Item' in response:
            return build_response(200, response['Item'])
        else:
            return build_response(404, 'Office not found')
    except ClientError as e:
        print('Error:', e.response['Error']['Message'])
        return build_response(400, e.response['Error']['Message'])

def get_offices():
    try:
        scan_params = {
            'TableName': office_table.name
        }
        return build_response(200, scan_dynamo_records(scan_params, []))
    except ClientError as e:
        print('Error:', e.response['Error']['Message'])
        return build_response(400, e.response['Error']['Message'])

def scan_dynamo_records(scan_params, item_array):
    response = office_table.scan(**scan_params)
    item_array.extend(response.get('Items', []))

    if 'LastEvaluatedKey' in response:
        scan_params['ExclusiveStartKey'] = response['LastEvaluatedKey']
        return scan_dynamo_records(scan_params, item_array)
    else:
        return {'offices': item_array}

def save_office(request_body):
    try:
        print('Saving office:', request_body)
        request_body['id'] = str(request_body['id'])
        office_table.put_item(Item=request_body)
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': request_body
        }
        return build_response(200, body)
    except ClientError as e:
        print('Error:', e.response['Error']['Message'])
        return build_response(400, e.response['Error']['Message'])

def modify_office(office_id, update_key, update_value):
    try:
        response = office_table.update_item(
            Key={'id': office_id},
            UpdateExpression=f'SET {update_key} = :value',
            ExpressionAttributeValues={':value': update_value},
            ReturnValues='UPDATED_NEW'
        )
        body = {
            'Operation': 'UPDATE',
            'Message': 'SUCCESS',
            'UpdatedAttributes': response['Attributes']
        }
        return build_response(200, body)
    except ClientError as e:
        print('Error:', e.response['Error']['Message'])
        return build_response(400, e.response['Error']['Message'])

def delete_office(office_id):
    try:
        response = office_table.delete_item(
            Key={'id': office_id},
            ReturnValues='ALL_OLD'
        )
        if 'Attributes' in response:
            body = {
                'Operation': 'DELETE',
                'Message': 'SUCCESS',
                'Item': response['Attributes']
            }
            return build_response(200, body)
        else:
            return build_response(404, 'Office not found')
    except ClientError as e:
        print('Error:', e.response['Error']['Message'])
        return build_response(400, e.response['Error']['Message'])

def create_office_transaction(request_body):
    try:
        required_fields = ['officeid', 'amount', 'transactionType']
        for field in required_fields:
            if field not in request_body:
                return build_response(400, f'Invalid request: Missing required field {field}')
        
        office_id = request_body['officeid']
        amount = request_body['amount']
        transaction_type = request_body['transactionType']

        if not isinstance(amount, (int, float)) or amount <= 0:
            return build_response(400, 'Invalid request: amount must be a positive number')
        
        if transaction_type not in ['EXPENSE', 'INCOME']:
            return build_response(400, 'Invalid request: transactionType must be either EXPENSE or INCOME')

        # Check if office exists
        office_response = office_table.get_item(Key={'id': office_id})
        if 'Item' not in office_response:
            return build_response(404, 'Office not found')

        # Add transaction to DynamoDB
        request_body['officeid'] = str(request_body['officeid'])  # Ensure officeid is string
        transaction_table.put_item(Item=request_body)
        
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': request_body
        }
        return build_response(200, body)
    except ClientError as e:
        print('Error:', e.response['Error']['Message'])
        return build_response(400, e.response['Error']['Message'])

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            if obj % 1 == 0:
                return int(obj)
            else:
                return float(obj)
        return super(DecimalEncoder, self).default(obj)

def build_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }
