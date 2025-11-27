import boto3
import json

def lambda_handler(event, context):
    dynamo_client = boto3.client("dynamodb")
    table_name = "Inventory"

    # Extract the item_id from path parameters
    if "pathParameters" not in event or "id" not in event["pathParameters"]:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing 'id' path parameter")
        }

    item_id = event["pathParameters"]["id"]

    # Scan to find the item (because table has composite key)
    try:
        scan_response = dynamo_client.scan(
            TableName=table_name,
            FilterExpression="item_id = :id",
            ExpressionAttributeValues={
                ":id": {"S": item_id}
            }
        )

        items = scan_response.get("Items", [])

        if len(items) == 0:
            return {
                "statusCode": 404,
                "body": json.dumps("Item not found")
            }

        item = items[0]

        return {
            "statusCode": 200,
            "body": json.dumps(item, default=str)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }