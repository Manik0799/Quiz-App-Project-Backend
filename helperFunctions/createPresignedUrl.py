from uploadImagesToS3 import s3, bucket_name
from botocore.exceptions import ClientError
import logging

def create_presigned_url(object_name, expiration=3600):

    # Generate a presigned URL for the S3 object
    try:
        response = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response