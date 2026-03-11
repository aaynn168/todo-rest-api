"""
CreateTodo Lambda Function
POST /todos - Create a new TODO item
"""

import json
import boto3
import uuid
from datetime import datetime

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todos')

def lambda_handler(event, context):
    """
    Create a new TODO item
    
    Request Body:
        {
            "title": "string" (required)
        }
    
    Response:
        201 - TODO created successfully
        400 - Invalid input
        500 - Server error
    """
    
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        # Validate input
        if 'title' not in body or not body['title']:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Title is required'})
            }
        
        # Create new TODO
        todo_id = str(uuid.uuid4())
        todo = {
            'id': todo_id,
            'title': body['title'],
            'completed': False,
            'created': datetime.now().isoformat()
        }
        
        # Save to DynamoDB
        table.put_item(Item=todo)
        
        print(f"Created TODO: {todo_id}")
        
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(todo)
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
