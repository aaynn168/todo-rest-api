"""
UpdateTodo Lambda Function
PUT /todos/{id} - Update a TODO item
"""

import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todos')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    """
    Update TODO item
    
    Path Parameters:
        id - TODO identifier
    
    Request Body:
        {
            "title": "string" (optional),
            "completed": boolean (optional)
        }
    
    Response:
        200 - TODO updated successfully
        400 - Invalid input
        500 - Server error
    """
    
    try:
        # Get ID from path
        todo_id = event['pathParameters']['id']
        
        # Parse body
        body = json.loads(event.get('body', '{}'))
        
        print(f"Updating TODO: {todo_id}")
        print(f"Update data: {body}")
        
        # Build update expression
        update_parts = []
        expr_values = {}
        expr_names = {}
        
        if 'title' in body:
            update_parts.append("#title = :title")
            expr_values[':title'] = body['title']
            expr_names['#title'] = 'title'
        
        if 'completed' in body:
            update_parts.append("completed = :completed")
            expr_values[':completed'] = body['completed']
        
        # If nothing to update
        if not update_parts:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'No fields to update'})
            }
        
        update_expr = "SET " + ", ".join(update_parts)
        
        # Update item
        response = table.update_item(
            Key={'id': todo_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_values,
            ExpressionAttributeNames=expr_names if expr_names else None,
            ReturnValues='ALL_NEW'
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response['Attributes'], cls=DecimalEncoder)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }
