# import json
# import boto3
#
# s3 = boto3.Session('s3')
# json_object = 'test_file.json'
# s3.put_object(
#      Body=json.dumps(json_object),
#      Bucket='teslaspectrajson',
#      Key='test_file.json'
# )
import boto3
from Tesla import settings


#create  a connection to S3 using boto3 and the AWS access keys hidden in settings.py
s3 = boto3.client('s3', aws_access_key_id = settings.aws_access_key_id,
                  aws_secret_access_key= settings.aws_secret_access_key)

#
# #download the contents of the bucket-stored json file to the local json file.
# with open("test_file.json", "wb") as f:
#     s3.download_fileobj("teslaspectrajson", "test_file.json", f)


#we have to open the local JSON file as a binary file before we can upload its contents
# to the bucket stored file
with open("test_file.json", "wb") as f:
    s3.download_fileobj("teslaspectrajson", "test_file.json", f)

