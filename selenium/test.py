# import json
# import boto3
#
# s3 = boto3.Session('s3')
# json_object = 'local_test_file.json'

import boto3
from Tesla import settings
import json

#create  a connection to S3 using boto3 and the AWS access keys hidden in settings.py
s3 = boto3.client('s3', aws_access_key_id = settings.aws_access_key_id,
                  aws_secret_access_key= settings.aws_secret_access_key)



# s3.put_object(
#      Body= json.dumps("local_test_file.json"),
#      Bucket='teslaspectrajson',
#      Key='test_file.json'
# )

#
# #download the contents of the bucket-stored json file to the local json file.
# with open("local_test_file.json", "wb") as f:
#     s3.download_fileobj("teslaspectrajson", "test_file.json", f)


with open("local_test_file.json", "rb") as readbinary:
    s3.upload_fileobj(readbinary, "teslaspectrajson", "test_file.json")

#we have to open the local JSON file as a binary file before we can upload its contents
# to the bucket stored file

# s3.upload_fileobj("local_test_file.txt", "teslaspectrajson", "test_file.txt")

