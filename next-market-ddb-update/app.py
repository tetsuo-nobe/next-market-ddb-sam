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
        body = json.loads(event["body"])
        p_email = body["email"]
        p_title = body["title"]
        p_price = body["price"]
        p_description = body["description"]
        p_image = body["image"]
        #
        msg = {}
        #
        # email を取得
        response = ddb.get_item(
            TableName = table_name,
            Key       = {
                         '_id': {'S': id}
            }
        )
        item = response.get("Item")
        email = item["email"]["S"]
        #
        # email が同じ場合は update する
        if p_email == email:
            item = {
                "_id":   {"S": id},
                "title": {"S": p_title},
                "price":  {"N": str(p_price)},
                "image": {"S": p_image},
                "description": {"S": p_description},
                "email": {"S": email}
            }
            ddb.put_item(TableName=table_name, Item=item)
            #
            # レスポンス用の Itemを作成
            singleItem = {
                "_id":   id,
                "title": p_title,
                "price": str(p_price),
                "image": p_image,
                "description": p_description,
                "email": p_email
            }
            msg = {"message": "アイテム編集成功","singleItem": singleItem}
        else:
            msg = {"message": "他の人が作成したアイテムです。"}
            
    except Exception as e:
        msg = {"message": "アイテム編集失敗"}
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
