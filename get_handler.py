import json

import boto3

headers = {
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Origin": '*',
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE"
}


def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("todo-app-tutorial")

    try:
        body = table.scan().get("Items", {})

        response = []
        for items in body:
            item = {
                "id": items["id"],
                "title": items["title"],
                "content": items["content"],
                "completed": items["completed"],
                "deadline": items["deadline"]
            }
            response.append(item)
        
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "items": response
            })
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "headers": headers
        }