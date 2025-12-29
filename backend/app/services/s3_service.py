import boto3
from botocore.exceptions import ClientError
from typing import Optional
import uuid

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
    try:
        client.put_object(
            Bucket=bucket,
            Key=key,
            Body=file_data,
            ContentType=content_type
        )
        # return f"https://{bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"
    except ClientError as e:
        print(f"S3 upload error: {e}")
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
    try:
        return client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=expiration
        )
    except ClientError as e:
        print(f"S3 presigned URL error: {e}")
        raise

