from django.conf import settings

from ...s3_service.s3_client import get_minio_client
from ...s3_service.s3_service import S3Service


class S3ServiceBaseConfigClass:
    def setUp(self):
        self.client = get_minio_client(
            endpoint=settings.MINIO_URL,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
        )

        self.bucket_name = "test-cloud-bucket"

        self.client.make_bucket(self.bucket_name)

        self.s3_service = S3Service(self.client, self.bucket_name)

    def tearDown(self):
        # Action for tear down tests: clear all object and remove bucket
        objects = self.client.list_objects(self.bucket_name, recursive=True)

        for obj in objects:
            self.client.remove_object(self.bucket_name, obj.object_name)

        self.client.remove_bucket(self.bucket_name)
