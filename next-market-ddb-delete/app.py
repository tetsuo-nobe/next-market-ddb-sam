import json
import boto3
import os

ddb = boto3.client("dynamodb")
table_name = os.environ["TABLE_NAME"]

def lambda_handler(event, context):
    try:
        id = event["pathParameters"]["id"]
        body = json.loads(event["body"])
        p_email = body["email"]
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
        # email が同じ場合は delete する
        if p_email == email:
            ddb.delete_item(
                TableName=table_name,
                Key       = {
                     '_id': {'S': id}
                }
            )
            msg = {"message": "アイテム削除成功"}
        else:
            msg = {"message": "他の人が作成したアイテムです。"}
            
    except Exception as e:
        msg = {"message": "アイテム削除失敗"}
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
