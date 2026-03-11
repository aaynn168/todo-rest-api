"""
DeleteTodo Lambda Function
DELETE /todos/{id} - Delete a TODO item
"""

import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todos')

def lambda_handler(event, context):
    """
    Delete TODO item
    
    Path Parameters:
        id - TODO identifier
    
    Response:
        200 - TODO deleted successfully
        500 - Server error
    """
    
    try:
        # Get ID from path
        todo_id = event['pathParameters']['id']
        
        print(f"Deleting TODO: {todo_id}")
        
        # Delete item
        table.delete_item(Key={'id': todo_id})
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'TODO deleted successfully',
                'id': todo_id
            })
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
