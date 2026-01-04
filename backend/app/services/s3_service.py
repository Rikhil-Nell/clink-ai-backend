import uuid

import boto3
import logfire
from botocore.exceptions import ClientError

from app.core.config import settings


client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)
bucket = settings.S3_BUCKET


def upload_file(
    file_data: bytes, 
    key: str, 
    content_type: str = "image/png"
) -> str | None:
    """
    Upload a file to S3.
    
    Args:
        file_data: The file contents as bytes
        key: The S3 object key (path) to upload to
        content_type: MIME type of the file
        
    Returns:
        The S3 URL of the uploaded file
    """
    with logfire.span("s3_upload", key=key, content_type=content_type, size_bytes=len(file_data)):
        try:
            client.put_object(
                Bucket=bucket,
                Key=key,
                Body=file_data,
                ContentType=content_type
            )
            url = f"https://{bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"
            logfire.debug("S3 upload success", url=url)
            return url
        except ClientError as e:
            logfire.error("S3 upload failed", key=key, exc_info=e)
            raise


def generate_coupon_key(loyalty_program_id: int, order_id: uuid.UUID, offer_variant: str) -> str:
    """Generate a unique S3 key for a coupon image."""
    unique_id = uuid.uuid4().hex[:8]
    return f"ai-offers/{loyalty_program_id}/{order_id}_{offer_variant}_{unique_id}.png"


def get_presigned_url(key: str, expiration: int = 3600) -> str:
    """
    Generate a presigned URL for temporary access to a private object.
    
    Args:
        key: The S3 object key
        expiration: URL expiration time in seconds (default 1 hour)
        
    Returns:
        Presigned URL string
    """
    with logfire.span("s3_presign", key=key, expiration=expiration):
        try:
            url = client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': key},
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            logfire.error("S3 presigned URL failed", key=key, exc_info=e)
            raise

