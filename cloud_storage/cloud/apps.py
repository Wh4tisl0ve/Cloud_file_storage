from django.apps import AppConfig
from django.conf import settings

from .s3_service.s3_service_factory import S3ServiceFactory


class CloudConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cloud"

    def ready(self):
        s3_factory = S3ServiceFactory(
            endpoint=settings.MINIO_URL,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False,
        )

        bucket_name = settings.MINIO_BUCKET_NAME

        self.s3_service = s3_factory.get_service(bucket_name)
