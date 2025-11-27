import boto3
import json

def lambda_handler(event, context):
    # DynamoDB setup
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    # Extract the item_id from the path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    item_id = event['pathParameters']['id']

    # First, scan the table to find the item (to get item_location_id)
    try:
        scan_response = dynamo_client.scan(
            TableName=table_name,
            FilterExpression="item_id = :id",
            ExpressionAttributeValues={
                ":id": {"S": item_id}
            }
        )

        items = scan_response.get('Items', [])

        if len(items) == 0:
            return {
                'statusCode': 404,
                'body': json.dumps(f"Item with ID {item_id} not found.")
            }

        # DynamoDB needs both keys: item_id AND item_location_id
        item = items[0]
        location_id = item["item_location_id"]["S"]

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error scanning for item: {str(e)}")
        }

    # Delete the item using full PK + SK
    try:
        dynamo_client.delete_item(
            TableName=table_name,
            Key={
                "item_id": {"S": item_id},
                "item_location_id": {"N": str(location_id)}
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {item_id} deleted successfully.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {str(e)}")
        }