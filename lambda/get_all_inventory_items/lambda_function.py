import json
import boto3

def lambda_handler(event, context):
    # DynamoDB setup
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Inventory")

    # Scan the table
    try:
        response = table.scan()
        items = response.get("Items", [])

        return {
            "statusCode": 200,
            "body": json.dumps(items, default=str)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error scanning table: {str(e)}")
        }