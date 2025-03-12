import json
import boto3
import os
import uuid
from aws_xray_sdk.core import patch
patch(['boto3'])          # Lambda関数から呼び出しているサービスのトレースを取得


ddb = boto3.client("dynamodb")
table_name = os.environ["TABLE_NAME"]

def lambda_handler(event, context):
    msg = {}
    try:
        # ファイルオープンとロード 
        f = open('item_data.json')
        items = json.load(f)  
        #
        for rec in items:
            id = str(uuid.uuid4())
            item = {
              "_id":   {"S": id},
              "title": {"S": rec["title"]},
              "price":  {"N": str(rec["price"])},
              "image": {"S": rec["image"]},
              "description": {"S": rec["description"]},
              "email": {"S": rec["email"]}
            }
            ddb.put_item(TableName=table_name, Item=item)
        
        # ファイルのクローズ
        f.close()
        msg = {"message": "JSONファイルからのデータのロードが完了しました"}

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
