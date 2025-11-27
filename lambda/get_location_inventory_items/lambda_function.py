import boto3
import json
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Inventory")

    # Extract the location_id from path parameters
    if "pathParameters" not in event or "id" not in event["pathParameters"]:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing 'id' path parameter (location_id)")
        }

    # Keep as string to match how it's stored
    location_id = event["pathParameters"]["id"]

    try:
        # Scan and filter by item_location_id
        response = table.scan(
            FilterExpression=Attr("item_location_id").eq(location_id)
        )

        items = response.get("Items", [])

        if not items:
            return {
                "statusCode": 404,
                "body": json.dumps(f"No items found for location_id {location_id}")
            }

        return {
            "statusCode": 200,
            "body": json.dumps(items, default=str)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error querying items: {str(e)}")
        }
