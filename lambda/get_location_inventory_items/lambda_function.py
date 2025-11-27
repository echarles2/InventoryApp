import boto3
import json

def lambda_handler(event, context):
    dynamo_client = boto3.client("dynamodb")
    table_name = "Inventory"
    index_name = "GSI_Location"  # Make sure this matches your actual GSI name

    # Extract the location_id from path parameters
    if "pathParameters" not in event or "id" not in event["pathParameters"]:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing 'id' path parameter (location_id)")
        }

    location_id = event["pathParameters"]["id"]

    # Query the GSI by item_location_id
    try:
        response = dynamo_client.query(
            TableName=table_name,
            IndexName=index_name,
            KeyConditionExpression="item_location_id = :loc",
            ExpressionAttributeValues={
                ":loc": {"N": str(location_id)}
            }
        )

        items = response.get("Items", [])

        if len(items) == 0:
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
    