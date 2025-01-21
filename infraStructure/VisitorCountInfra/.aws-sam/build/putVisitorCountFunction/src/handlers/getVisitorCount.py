import boto3
import json

def getVisitorCountHandler(event, context):
    # Initialize the DynamoDB client
    dynamodb = boto3.resource('dynamodb')

    # Replace 'YourTableName' with your DynamoDB table name
    table_name = 'VisitorCountTable'
    table = dynamodb.Table(table_name)

    try:
        # Query the DynamoDB table
        response = table.get_item(Key={'visitors': 'visitorCount'})  # Replace 'primaryKey' with your actual primary key name
        response['Item']['count'] = int(response['Item']['count'])  # Convert Decimal to int
        # Check if the item exists

        if 'Item' in response:

            return {
                'statusCode': 200,
                'headers': {
                "Access-Control-Allow-Headers" : "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*" ,
                "Accept":'*/*',
                "Content-Type":'application/json',
                'Vary:':'Origin'

            },
                'body': json.dumps({'visitorCount':response['Item']['count']})
            }
        else:
            return {
                'statusCode': 404,
                'headers': {
                "Access-Control-Allow-Headers" : "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*" ,
                "Accept":'*/*',
                "Content-Type":'application/json',
                'Vary:':'Origin'

            },
                'body': json.dumps('Item not found.')
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                "Access-Control-Allow-Headers" : "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*" ,
                "Accept":'*/*',
                "Content-Type":'application/json',
                'Vary:':'Origin'
            },
            'body': json.dumps(f"Error retrieving item: {str(e)}")
        }
