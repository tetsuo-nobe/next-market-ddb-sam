import json
import boto3
import os
import uuid
from aws_xray_sdk.core import patch
patch(['boto3'])          # Lambda関数から呼び出しているサービスのトレースを取得


ddb = boto3.client("dynamodb")
table_name = os.environ["TABLE_NAME"]

def lambda_handler(event, context):
    try:
        id = str(uuid.uuid4())
        body = json.loads(event["body"])
        p_email = body["email"]
        p_title = body["title"]
        p_price = body["price"]
        p_description = body["description"]
        p_image = body["image"]
        #
        msg = {}
        
        item = {
            "_id":   {"S": id},
            "title": {"S": p_title},
            "price":  {"N": str(p_price)},
            "image": {"S": p_image},
            "description": {"S": p_description},
            "email": {"S": p_email}
        }
        ddb.put_item(TableName=table_name, Item=item)
        #
        msg = {"message": "アイテム作成成功"}

    except Exception as e:
        msg = {"message": "アイテム作成失敗"}
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
