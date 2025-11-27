import boto3
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Inventory")

    # Extract the item_id from the path parameters
    if "pathParameters" not in event or "id" not in event["pathParameters"]:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing 'id' path parameter")
        }

    item_id = event["pathParameters"]["id"]

    try:
        # Optional: check if the item exists first
        response = table.get_item(Key={"item_id": item_id})
        if "Item" not in response:
            return {
                "statusCode": 404,
                "body": json.dumps(f"Item with ID {item_id} not found.")
            }

        # Delete using only the primary key (item_id)
        table.delete_item(Key={"item_id": item_id})

        return {
            "statusCode": 200,
            "body": json.dumps(f"Item with ID {item_id} deleted successfully.")
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error deleting item: {str(e)}")
        }
