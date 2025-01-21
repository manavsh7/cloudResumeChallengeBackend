import json
import boto3
from botocore.exceptions import ClientError
# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')

def putVisitorCountHandler(event, context):
    primary_key_value = 'visitorCount'  
    
        
            # Name of the DynamoDB table
    table_name = 'VisitorCountTable'  # Replace with your DynamoDB table name

    # Reference to the DynamoDB table
    table = dynamodb.Table(table_name)
    try:
    # Update the item in DynamoDB
        response = table.update_item(
            Key={
                'visitors': primary_key_value  # Assuming 'primary_key' is the name of the primary key
            },
            UpdateExpression="ADD #count :increment",
            ExpressionAttributeNames={
                '#count': 'count'  # The attribute to increment
            },
            ExpressionAttributeValues={
                ':increment': 1  # Increment value
            },
            ReturnValues="UPDATED_NEW"  
        )
    
    # Get the updated visitor count
        updated_count = int(response['Attributes']['count'])  # Convert Decimal to int
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                'Content-Type': 'application/json',
                'Vary:':'Origin'


            },
            'body': json.dumps({
                'message': 'Visitor count incremented successfully',
                'visitorCount': updated_count
            })
        }
    

    except ClientError as e:
    # Handle errors (e.g., item not found, permission issues)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                'Content-Type': 'application/json',
                'Vary:':'Origin'


            },
            'body': json.dumps({
                'error': str(e)
            })
        }







    

