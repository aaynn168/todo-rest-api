"""
GetAllTodos Lambda Function
GET /todos - Retrieve all TODO items
"""

import json
import boto3
from decimal import Decimal

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todos')

# Helper to convert Decimal to native types
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    """
    Get all TODO items
    
    Response:
        200 - Success with list of TODOs
        500 - Server error
    """
    
    try:
        # Scan table (get all items)
        response = table.scan()
        todos = response.get('Items', [])
        
        # Sort by created date (newest first)
        todos.sort(key=lambda x: x.get('created', ''), reverse=True)
        
        print(f"Retrieved {len(todos)} TODOs")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'todos': todos,
                'count': len(todos)
            }, cls=DecimalEncoder)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }
