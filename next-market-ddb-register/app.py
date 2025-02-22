import json
import boto3
import os

ddb = boto3.client("dynamodb")
table_name = os.environ["TABLE_NAME"]

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        email = body["email"]
        password = body["password"]
        name = body["name"]
        #print(email)
        #print(password)
        #print(name)
        msg = {}
        #
        item = {
                "email": {"S": email},
                "name": {"S": name},
                "password": {"S": password}
        }
        ddb.put_item(TableName=table_name, Item=item)
        msg = {"message": "ユーザー登録成功"}
    except Exception as e:
        msg = {"message": "ユーザー登録失敗"}
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
