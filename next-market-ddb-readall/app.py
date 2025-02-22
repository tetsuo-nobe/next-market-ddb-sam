import json
import boto3
import os

ddb = boto3.client("dynamodb")
table_name = os.environ["TABLE_NAME"]

def lambda_handler(event, context):
    try:
        msg = {}
        #
        response = ddb.scan(TableName=table_name)
        ddb_formats_items = response.get("Items",[])
        allItems = []
        for item in ddb_formats_items:
            formated_item = {
                    "_id": item["_id"]["S"],
                    "title": item["title"]["S"],
                    "image": item["image"]["S"],
                    "price": item["price"]["N"],
                    "description": item["description"]["S"]
            }
            allItems.append(formated_item)
        msg = {"message": "アイテム読み取り成功（オール）","allItems": allItems}
    except Exception as e:
        msg = {"message": "アイテム読み取り失敗（オール）"}
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
