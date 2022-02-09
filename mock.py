import boto3
import urllib.parse
import base64
import os


# domein
DOMAIN_NAME = os.environ["DOMAIN_NAME"]
# bucket_name
BUCKET_NAME = os.environ["BUCKET_NAME"]
# forwarding
FOREWARD_MAIL = os.environ["FOREWARD_MAIL"]
# region
REGION = os.environ["REGION"]
ses_client = boto3.client('ses',region_name=REGION)
s3 = boto3.resource('s3')


def lambda_handler(event, context):

    print("-event----------")
    print(event)

    ses_client = boto3.client('ses',region_name=REGION)
    s3_client = boto3.client('s3')
    message_id = event['Records'][0]['ses']['mail']['messageId']
    response = s3_client.get_object(
        Bucket = BUCKET_NAME,
        Key    = message_id
    )

    MAIL_FROM = 'lambdaAgent' + "@" + DOMAIN_NAME
    print("-response!----------")
    print(response)
    print("-responseBody!----------")
    mail = response['Body'].read().decode('utf-8').replace('\n','').replace('\r','')
    print(mail)
    body = base64.b64decode(mail.split('base64')[1].split('--')[0])
    print("-responseBodyText!----------")
    print(body.decode('utf-8'))
    d_body = body.decode('utf-8')
    print("-subject----------")
    subject = mail.split('Subject: ')[1].split('To: ')[0]
    print(subject)

    response = ses_client.send_email(
        Source=MAIL_FROM,
        Destination={
            'ToAddresses': [
                FOREWARD_MAIL,
            ]
        },
        Message={
            'Subject': {
                'Data': subject,
            },
            'Body': {
                'Text': {
                    'Data': 'Reservation waiting for cancellation.\nCompleted successfully',
                },
            }
        }
    )

    print("object deleted..")
    # bucket, key
    s3_client.delete_object(Bucket=BUCKET_NAME, Key=message_id)

    return
