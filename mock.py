import boto3
import json
import re
import urllib.parse
import base64
from boto3.session import Session
import os
import email
from email.header import decode_header


#転送メールの送信元ドメイン名
DOMAIN_NAME = os.environ["DOMAIN_NAME"]
# bucket_name
BUCKET_NAME = os.environ["BUCKET_NAME"]
# forwarding
FOREWARD_MAIL = os.environ["FOREWARD_MAIL"]
# region
reg_name = os.environ["REGION"]
# S3 高レベルAPI
s3 = boto3.resource('s3')


# # メールの件名を取得
# def get_email_subject(email_object):
#     (subject, subject_charaset) = decode_header(email_object['Subject'])[0]

#     if subject_charaset == None:
#         email_subject = subject
#     else:
#         email_subject = subject.decode(subject_charaset)

#     print("Email Subject: %s" % email_subject)
#     return email_subject



# def lambda_handler(event, context):
#     print("-1----------")
#     print(event)
#     # バケット名取得
#     bucket = event['Records'][0]['s3']['bucket']['name']
#     # オブジェクトのkey取得
#     key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
#     # オブジェクトを取得する
#     s3_object = s3.Object(bucket, key)
#     print(s3_object)
#     response = s3_object.get()
#     print("-response!----------")
#     print(response)
#     print("-responseBody!----------")
#     mail = response['Body'].read().decode('utf-8').replace('\n','').replace('\r','')
#     print(mail)
#     body = base64.b64decode(mail.split('base64')[1].split('--')[0])
#     print("-responseBodyText!----------")
#     print(body.decode('utf-8'))
#     d_body = body.decode('utf-8')
#     # ここまでは確定
#     # 検証中
#     print("-4----------")
#     subject = mail.split('Subject: ')[1].split('To: ')[0]
#     print(subject)

#     client = boto3.client('ses',region_name=reg_name)
#     response = client.send_email(
#         Source=FOREWARD_MAIL,
#         Destination={
#             'ToAddresses': [
#                 FOREWARD_MAIL,
#             ]
#         },
#         Message={
#             'Subject': {
#                 'Data': subject,
#             },
#             'Body': {
#                 'Text': {
#                     'Data': d_body,
#                 },
#             }
#         }
#     )

#     return

def lambda_handler(event, context):
    print("-1----------")
    print(event)
    ses_client = boto3.client('ses',region_name=reg_name)
    s3_client = boto3.client('s3')
    message_id = event['Records'][0]['ses']['mail']['messageId']
    res3 = s3_client.get_object(
        Bucket = BUCKET_NAME,
        Key    = message_id
    )
    print("-2----------")
    raw_message = res3['Body'].read()
    #本来の送信者
    MAIL_SOURCE = event['Records'][0]['ses']['mail']['source']
    print(MAIL_SOURCE)
    # #転送メールの送信者
    MAIL_FROM = MAIL_SOURCE.replace('@','=') + "@" + DOMAIN_NAME
    print(MAIL_FROM)
    print("-3----------")
    ses_client.send_raw_email(
        Source = FOREWARD_MAIL,
        Destinations=[
            FOREWARD_MAIL
        ],
        RawMessage={
            'Data': raw_message
        }
    )

    return