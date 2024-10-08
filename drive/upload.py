import os
from dotenv import load_dotenv
import boto3
import math
from botocore.client import ClientError

load_dotenv()

AWS_BUCKET = os.getenv('AWS_BUCKET')
AWS_REGION = os.getenv('AWS_REGION')
AWS_KEY = os.getenv('AWS_KEY')
AWS_SECRET = os.getenv('AWS_SECRET')

s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_KEY,
        aws_secret_access_key=AWS_SECRET,
        region_name=AWS_REGION,
    )

try:
    s3.head_bucket(Bucket=AWS_BUCKET)
except ClientError:
    s3.create_bucket(
        Bucket=AWS_BUCKET, 
        CreateBucketConfiguration={'LocationConstraint': AWS_REGION}
    )
                                                                                         # 50mb          
def get_presigned_urls(key: str, content_type: str, file_size: int, expire_in=900, chunk_size=5 * 1024**2): 
    # Key: obj key (or filename) within bucket. 
    #      a unique id for the obj in the bucket and can incl a path (similar to a filepath on a filesystem).
    total_chunks = math.ceil(file_size / chunk_size)
    print(total_chunks, ':D')

    payload = {
        'Bucket': AWS_BUCKET,
        'Key': key,
        'ContentType': content_type,
    }

    # initiate a multipart upload
    data = s3.create_multipart_upload(**payload)
    upload_id = data['UploadId']
    urls = []

    print(data, 'dd')

    # create pre-signed URLs for each part
    for part_no in range(1, total_chunks + 1):
        signed_url = s3.generate_presigned_url(
            ClientMethod='upload_part',
            Params={
                'Bucket': AWS_BUCKET,
                'Key': key,
                'UploadId': upload_id,
                'PartNumber': part_no
            },
            ExpiresIn=expire_in,
        )
        urls.append(signed_url)

    return {
        'urls': urls,
        'chunk_size': chunk_size,
        'key': key,
        'upload_id':upload_id,
        'content_type': content_type
    }

def save_etags(key: str, upload_id: str, etags_string: str):
    etags = etags_string.split(',')

    parts = [{'ETag': etags[i], 'PartNumber': i + 1} for i in range(len(etags))]

    res = s3.complete_multipart_upload(
        Bucket=AWS_BUCKET,
        Key=key,
        UploadId=upload_id,
        MultipartUpload={'Parts': parts},
    )

    print('-.-', res)

    return { 'location' : res['Location'] }
