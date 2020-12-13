import boto3
import os

AWS_REGION_NAME=os.environ.get('AWS_REGION_NAME', None)
AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY', None)

DB_NAME=os.environ.get('DB_NAME', None)
DB_HOST=os.environ.get('DB_HOST', None)
DB_USER=os.environ.get('DB_USER', None)
DB_PASSWORD=os.environ.get('DB_PASSWORD', None)

BUCKET_NAME = os.environ.get('BUCKET_NAME', None)
DUMP_NAME = os.environ.get('DUMP_NAME', None)
LOCAL_DUMP_NAME = "lw-dump.sql"

s3 = boto3.client('s3',
                  region_name=AWS_REGION_NAME,
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                  )

s3.download_file(BUCKET_NAME, DUMP_NAME, LOCAL_DUMP_NAME)

restore_dump_cmd = f'mysql -h {DB_HOST} -u {DB_USER} --password={DB_PASSWORD} {DB_NAME} < {LOCAL_DUMP_NAME}'
os.system(restore_dump_cmd)
