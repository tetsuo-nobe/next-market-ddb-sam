import json
import jwt
import boto3
import os
from aws_xray_sdk.core import patch
patch(['boto3'])          # Lambda関数から呼び出しているサービスのトレースを取得

# import requests

ddb = boto3.client("dynamodb")
table_name = os.environ["TABLE_NAME"]

def lambda_handler(event, context):
    body = json.loads(event["body"])
    email = body["email"]
    password = body["password"]
    #print(email)
    #print(password)
    msg = {}
    #
    response = ddb.get_item(
            TableName = table_name,
            Key       = {
                         'email': {'S': email}
            }
    )
    
    # ユーザーが存在しない場合
    item = response.get("Item","no-key")
    if item == "no-key":
        msg = {"message": "ログイン失敗：ユーザーを登録して下さい。"}
    else:
    # ユーザーが存在する場合    
        # パスワードチェック
        ddb_password =  item["password"]["S"]
        if password != ddb_password:
            msg = {"message": "ログイン失敗：パスワードが間違っています。"}
        else:
            # JWTの生成
            payload = {"email": email}
            secret = 'next-market-app-book'
            token = jwt.encode(payload, secret, algorithm='HS256')
            print(token)  # 生成されたJWTを表示
            msg = {"message": "ログイン成功", "token": token}
    
            # JWTの検証
            # try:
            #     decoded = jwt.decode(token, secret, algorithms=['HS256'])
            #     print(decoded)  # デコードされたペイロードを表示
            # except jwt.ExpiredSignatureError:
            #     print('トークンの有効期限切れ')
            # except jwt.InvalidTokenError:
            #     print('無効なトークン')
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
