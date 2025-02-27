import json
import boto3
import os
from aws_xray_sdk.core import patch
patch(['boto3'])          # Lambda関数から呼び出しているサービスのトレースを取得

ddb = boto3.client("dynamodb")
table_name = os.environ["TABLE_NAME"]

def lambda_handler(event, context):
    try:
        id = event["pathParameters"]["id"]
        msg = {}
        #
        response = ddb.get_item(
            TableName = table_name,
            Key       = {
                         '_id': {'S': id}
            }
        )
        item = response.get("Item")
        formated_item = {
            "_id": item["_id"]["S"],
            "title": item["title"]["S"],
            "image": item["image"]["S"],
            "price": item["price"]["N"],
            "description": item["description"]["S"],
            "email": item["email"]["S"]
        }
        msg = {"message": "アイテム読み取り成功（シングル）","singleItem": formated_item}
    except Exception as e:
        msg = {"message": "アイテム読み取り成功（シングル）"}
        print(f"予期しないエラーが発生しました: {e}")

    #
    return {
        "statusCode": 200,
        "body": json.dumps(msg,
          ensure_ascii=False
        ),
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "application/json; charset=UTF-8",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "PUT,GET,POST,DELETE,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type,X-CSRF-TOKEN"
         }
    }
