"""
=====================================
 aws_libs/s3_service.py
 Custom S3 Library for Recipe Cloud
=====================================
Wraps all boto3 S3 operations used across the project.
Usage:
    from aws_libs.s3_service import S3Service
    s3 = S3Service()
    s3.upload_csv(content_bytes, "backups/user_posts.csv")
    url = s3.get_file_url("backups/user_posts.csv")
"""

import boto3
from botocore.exceptions import ClientError
from django.conf import settings


class S3Service:
    """
    Custom library for all Amazon S3 operations in Recipe Cloud.
    Covers:
      - Uploading CSV exports to S3
      - Uploading media files (images/videos)
      - Generating public/pre-signed URLs
      - Deleting files from S3
    """

    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        self.export_bucket = getattr(
            settings, "AWS_EXPORT_BUCKET_NAME", self.bucket_name
        )
        self.region = settings.AWS_S3_REGION_NAME

    # ─── CSV EXPORT ───────────────────────────────────────────────
    def upload_csv(self, content_bytes: bytes, s3_key: str) -> dict:
        """
        Upload a CSV file to the export S3 bucket.

        Args:
            content_bytes (bytes): Raw CSV content.
            s3_key (str): S3 object key, e.g. "backups/john_posts.csv"

        Returns:
            dict: {"success": True, "key": s3_key, "url": public_url}
                  or {"success": False, "error": message}
        """
        try:
            self.client.put_object(
                Bucket=self.export_bucket,
                Key=s3_key,
                Body=content_bytes,
                ContentType="text/csv",
            )
            url = self._build_public_url(self.export_bucket, s3_key)
            return {"success": True, "key": s3_key, "url": url}
        except ClientError as e:
            return {"success": False, "error": str(e)}

    # ─── MEDIA FILE UPLOAD ────────────────────────────────────────
    def upload_media_file(
        self, file_obj, s3_key: str, content_type: str = "image/jpeg"
    ) -> dict:
        """
        Upload a media file (image/video) to S3.

        Args:
            file_obj: File-like object (e.g. from request.FILES).
            s3_key (str): S3 object key, e.g. "posts/recipe.jpg"
            content_type (str): MIME type of the file.

        Returns:
            dict: {"success": True, "key": s3_key, "url": public_url}
                  or {"success": False, "error": message}
        """
        try:
            self.client.upload_fileobj(
                file_obj,
                self.bucket_name,
                s3_key,
                ExtraArgs={"ContentType": content_type},
            )
            url = self._build_public_url(self.bucket_name, s3_key)
            return {"success": True, "key": s3_key, "url": url}
        except ClientError as e:
            return {"success": False, "error": str(e)}

    # ─── PRESIGNED URL ────────────────────────────────────────────
    def get_presigned_url(self, s3_key: str, expiry_seconds: int = 3600) -> str | None:
        """
        Generate a pre-signed URL for temporary private access.

        Args:
            s3_key (str): S3 object key.
            expiry_seconds (int): URL expiry time (default 1 hour).

        Returns:
            str: Pre-signed URL, or None on failure.
        """
        try:
            url = self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": s3_key},
                ExpiresIn=expiry_seconds,
            )
            return url
        except ClientError:
            return None

    # ─── DELETE FILE ──────────────────────────────────────────────
    def delete_file(self, s3_key: str, bucket: str = None) -> dict:
        """
        Delete a file from S3.

        Args:
            s3_key (str): S3 object key to delete.
            bucket (str): Target bucket (defaults to media bucket).

        Returns:
            dict: {"success": True} or {"success": False, "error": message}
        """
        target_bucket = bucket or self.bucket_name
        try:
            self.client.delete_object(Bucket=target_bucket, Key=s3_key)
            return {"success": True}
        except ClientError as e:
            return {"success": False, "error": str(e)}

    # ─── LIST FILES ───────────────────────────────────────────────
    def list_files(self, prefix: str = "", bucket: str = None) -> list:
        """
        List all files in the bucket under a given prefix.

        Args:
            prefix (str): Folder/prefix to filter, e.g. "backups/".
            bucket (str): Target bucket (defaults to media bucket).

        Returns:
            list: List of S3 object keys.
        """
        target_bucket = bucket or self.bucket_name
        try:
            response = self.client.list_objects_v2(Bucket=target_bucket, Prefix=prefix)
            return [obj["Key"] for obj in response.get("Contents", [])]
        except ClientError:
            return []

    # ─── INTERNAL HELPER ─────────────────────────────────────────
    def _build_public_url(self, bucket: str, key: str) -> str:
        return f"https://{bucket}.s3.{self.region}.amazonaws.com/{key}"
