from django.apps import AppConfig
from django.conf import settings

from .s3_service.s3_client import get_minio_client
from .s3_service.s3_service import S3Service


class CloudConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cloud"

    def ready(self):
        minio_client = get_minio_client(
            endpoint=settings.MINIO_URL,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
        )

        bucket_name = settings.MINIO_BUCKET_NAME

        self.s3_service = S3Service(minio_client, bucket_name)
