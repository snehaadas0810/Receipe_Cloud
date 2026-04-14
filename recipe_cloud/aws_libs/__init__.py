"""
aws_libs — Custom AWS Service Libraries for Recipe Cloud
=========================================================

Lightweight initializer to avoid unnecessary imports.

Recommended usage:
    from aws_libs.s3_service import S3Service
    from aws_libs.storage_service import StorageService
"""

# ✅ Import ONLY stable / commonly used services
from .s3_service import S3Service
from .storage_service import StorageService

__all__ = [
    "S3Service",
    "StorageService",
]
