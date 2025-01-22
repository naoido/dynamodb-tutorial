import json
import uuid

import boto3

headers = {
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Origin": '*',
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE"
}


def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("todo-app-tutorial")

    params = validate_params(event, ["title", "content", "deadline"])
    if params is None:
        return {
            "statusCode": 400,
            "headers": headers
        }
    
    task_id = str(uuid.uuid4())
    try:
        table.put_item(
                Item={
                    "id": task_id,
                    "title": params["title"],
                    "content": params["content"],
                    "completed": False,
                    "deadline": params["deadline"]
                })

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "task_id": task_id
            })
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "headers": headers
        }


def validate_params(event: dict[any, any], requires: list[str]) -> dict[str, any] | None:
    """
    必要なパラメータが入っているか検証します

    Args:
        event (dict): Lambdaのeventオブジェクト
        requires (list[str]): 必要なパラメータ名が入ったリスト
    
    Returns:
        dict[str, any]: リクエストのbodyのdictを返します
        None: リクエストが正しくない、もしくは空の場合に返されます
    """
    method = event.get("httpMethod")
    match method:
        case "GET" | "DELETE":
            body = event.get("queryStringParameters")
        case "POST" | "PUT":
            body = event.get("body")
            if body is None:
                return None
            body = json.loads(body)
        case _:
            return None

    return body if all(key in body.keys() for key in requires) else None