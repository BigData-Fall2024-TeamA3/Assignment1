# Create a session with explicit credentials
import boto3
session = boto3.Session(
    aws_access_key_id='Deepak_admin',
    aws_secret_access_key='AKIAZI2LIWOWP7ACGSWH',
#     aws_secret_access_key='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',
    region_name='us-east-2'
)

# Use the session to create a client for an AWS service
s3 = session.client('s3')

