"""
=====================================
 aws_libs/storage_service.py
 Custom Storage Library for Recipe Cloud
=====================================
Wraps django-storages S3 backend and provides
utility functions for media file handling with S3.

Usage:
    from aws_libs.storage_service import StorageService
    storage = StorageService()
    url = storage.get_media_url("posts/recipe.jpg")
    exists = storage.file_exists("posts/recipe.jpg")
"""


import boto3
from botocore.exceptions import ClientError
from django.conf import settings


class StorageService:
    """
    Custom library for S3-backed media file storage in Recipe Cloud.
    Works alongside django-storages DEFAULT_FILE_STORAGE.
    Covers:
      - Building public media URLs
      - Checking file existence in S3
      - Deleting media files when posts are deleted
      - Listing all media uploads for a specific user
    """

    def __init__(self):
        self.bucket = settings.AWS_STORAGE_BUCKET_NAME
        self.region = settings.AWS_S3_REGION_NAME
        self.base_url = f"https://{self.bucket}.s3.{self.region}.amazonaws.com"
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=self.region,
        )

    # ─── GET MEDIA URL ────────────────────────────────────────────
    def get_media_url(self, s3_key: str) -> str:
        """
        Build the full public URL for a media file stored in S3.

        Args:
            s3_key (str): e.g. "posts/recipe.jpg"

        Returns:
            str: Full public S3 URL.
        """
        return f"{self.base_url}/{s3_key}"

    # ─── FILE EXISTS ──────────────────────────────────────────────
    def file_exists(self, s3_key: str) -> bool:
        """
        Check whether a file exists in the S3 media bucket.

        Args:
            s3_key (str): S3 object key.

        Returns:
            bool: True if file exists.
        """
        try:
            self.client.head_object(Bucket=self.bucket, Key=s3_key)
            return True
        except ClientError:
            return False

    # ─── DELETE MEDIA FILE ────────────────────────────────────────
    def delete_media_file(self, s3_key: str) -> dict:
        """
        Delete a media file from S3 when a Post is deleted.

        Args:
            s3_key (str): S3 object key to delete.

        Returns:
            dict: {"success": True} or {"success": False, "error": message}
        """
        try:
            self.client.delete_object(Bucket=self.bucket, Key=s3_key)
            return {"success": True}
        except ClientError as e:
            return {"success": False, "error": str(e)}

    # ─── LIST USER MEDIA ──────────────────────────────────────────
    def list_user_media(self, username: str) -> list:
        """
        List all media files uploaded by a specific user.
        Assumes files are stored under "posts/" prefix.

        Args:
            username (str): Django username.

        Returns:
            list: List of dicts with key, size, last_modified.
        """
        try:
            response = self.client.list_objects_v2(Bucket=self.bucket, Prefix="posts/")
            files = []
            for obj in response.get("Contents", []):
                files.append(
                    {
                        "key": obj["Key"],
                        "size_kb": round(obj["Size"] / 1024, 2),
                        "last_modified": obj["LastModified"].strftime("%Y-%m-%d %H:%M"),
                        "url": self.get_media_url(obj["Key"]),
                    }
                )
            return files
        except ClientError:
            return []

    # ─── GET FILE METADATA ────────────────────────────────────────
    def get_file_metadata(self, s3_key: str) -> dict:
        """
        Return metadata for a specific file in S3.

        Args:
            s3_key (str): S3 object key.

        Returns:
            dict: {"key", "size_kb", "content_type", "last_modified"}
                  or {"error": message}
        """
        try:
            head = self.client.head_object(Bucket=self.bucket, Key=s3_key)
            return {
                "key": s3_key,
                "size_kb": round(head["ContentLength"] / 1024, 2),
                "content_type": head.get("ContentType", "unknown"),
                "last_modified": head["LastModified"].strftime("%Y-%m-%d %H:%M"),
            }
        except ClientError as e:
            return {"error": str(e)}
