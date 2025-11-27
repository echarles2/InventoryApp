import boto3
import json
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Inventory")

    if "pathParameters" not in event or "id" not in event["pathParameters"]:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing 'id' path parameter")
        }

    item_id = event["pathParameters"]["id"]

    try:

        scan_resp = table.scan(
            FilterExpression=Attr("item_id").eq(item_id)
        )
        items = scan_resp.get("Items", [])

        if not items:
            return {
                "statusCode": 404,
                "body": json.dumps(f"Item with ID {item_id} not found.")
            }

        item = items[0]
        location_id = item["item_location_id"]

        table.delete_item(
            Key={
                "item_id": item_id,
                "item_location_id": location_id
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps(f"Item with ID {item_id} deleted successfully.")
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error deleting item: {str(e)}")
        }
