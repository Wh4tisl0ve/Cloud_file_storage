import io
import minio

from unittest import TestCase
from django.conf import settings

from ..s3_service.s3_client import get_minio_client
from ..s3_service.s3_service import S3Service


class S3ServiceTestCase(TestCase):
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

    def test_create_directory(self):
        # Test case: Create empty "directory"
        user_id = 1
        directory_name = "test/"

        self.s3_service.create_object(user_id, object_name=directory_name)
        object_path = self.s3_service.create_path(user_id, directory_name)

        target_object = self.client.stat_object(self.bucket_name, object_path)
        self.assertEqual(object_path, target_object.object_name)

    def test_create_nested_directory(self):
        # Test case: Create directory hierarchy
        """
        test-cloud-bucket/
        ├─ test/
        │  ├─ teh/
        │  │  ├─ heh/
        │  │  ├─ teh/
        """
        user_id = 1
        directory_hierarchy = [
            f"user-{user_id}-files/test/",
            f"user-{user_id}-files/test/teh/",
            f"user-{user_id}-files/test/teh/heh/",
            f"user-{user_id}-files/test/teh/teh/",
        ]

        self.s3_service.create_object(user_id, object_name="test/")
        self.s3_service.create_object(
            user_id, object_name="teh/", current_directory="test"
        )
        self.s3_service.create_object(
            user_id, object_name="heh/", current_directory="test/teh"
        )
        self.s3_service.create_object(
            user_id, object_name="teh/", current_directory="test/teh"
        )

        all_directories = self.client.list_objects(
            self.bucket_name, start_after="test/", recursive=True
        )

        for directory in all_directories:
            self.assertIn(directory.object_name, directory_hierarchy)

    def test_delete_directory(self):
        # Test case: Delete empty "directory"
        user_id = 1
        directory_name = "test/"

        self.s3_service.create_object(user_id, object_name=directory_name)
        object_path = self.s3_service.create_path(user_id, directory_name)

        self.s3_service.delete_object(1, object_name=directory_name)

        self.assertRaises(
            minio.error.S3Error, self.client.stat_object, self.bucket_name, object_path
        )

    def test_create_file(self):
        # Test case: Create file text object in directory
        user_id = 1
        directory_name = "test"
        object_name = "test.txt"

        self.s3_service.create_object(
            user_id,
            object_name=object_name,
            current_directory=directory_name,
            data=io.BytesIO(b"test"),
        )

        object_path = self.s3_service.create_path(user_id, object_name, directory_name)

        target_object = self.client.stat_object(self.bucket_name, object_path)
        self.assertEqual(object_path, target_object.object_name)

    def test_delete_file(self):
        # Test case: Delete file text object in directory
        user_id = 1
        directory_name = "test"
        object_name = "test.txt"

        self.s3_service.create_object(
            user_id,
            object_name=object_name,
            current_directory=directory_name,
            data=io.BytesIO(b"test"),
        )

        object_path = self.s3_service.create_path(user_id, object_name, directory_name)

        self.s3_service.delete_object(
            user_id, object_name=object_name, current_directory=directory_name
        )

        self.assertRaises(
            minio.error.S3Error, self.client.stat_object, self.bucket_name, object_path
        )

    def test_rename_file(self):
        # Test case: Rename file text object in directory
        user_id = 1
        directory_name = "test"
        object_name = "test.txt"

        new_object_name = "test2.txt"

        self.s3_service.create_object(
            user_id,
            object_name=object_name,
            current_directory=directory_name,
            data=io.BytesIO(b"test"),
        )

        old_object_path = self.s3_service.create_path(
            user_id, object_name, directory_name
        )
        new_object_path = self.s3_service.create_path(
            user_id, new_object_name, directory_name
        )

        self.s3_service.rename_object(
            user_id, object_name, new_object_name, directory_name
        )

        target_object = self.client.stat_object(self.bucket_name, new_object_path)

        # old object deleted
        with self.assertRaises(minio.error.S3Error):
            self.client.stat_object(self.bucket_name, old_object_path)
            
        # new object created
        self.assertEqual(new_object_path, target_object.object_name)

    def test_rename_nested_directories(self):
        # Test case: Rename folder "test" with nested hierarchy directories
        # for hierarchy:
        """
        test-cloud-bucket/
        ├─ test/
        │  ├─ teh/
        │  │  ├─ heh/
        │  │  ├─ teh/
        """
        user_id = 1
        original_hierarchy = [
            f"user-{user_id}-files/test/",
            f"user-{user_id}-files/test/teh/",
            f"user-{user_id}-files/test/teh/heh/",
            f"user-{user_id}-files/test/teh/teh/",
        ]
        expected_hierarchy = [
            f"user-{user_id}-files/test5/",
            f"user-{user_id}-files/test5/teh/",
            f"user-{user_id}-files/test5/teh/heh/",
            f"user-{user_id}-files/test5/teh/teh/",
        ]
        for directory in original_hierarchy:
            self.client.put_object(self.bucket_name, directory, io.BytesIO(b""), 0)

        self.s3_service.rename_object(1, old_name="test/", new_name="test5/")

        all_directories = self.client.list_objects(
            self.bucket_name, start_after="test/", recursive=True
        )

        # old hierarchy deleted
        for directory in original_hierarchy:
            with self.assertRaises(minio.error.S3Error):
                self.client.stat_object(self.bucket_name, directory)

        # new hierarchy created
        for directory in all_directories:
            self.assertIn(directory.object_name, expected_hierarchy)
