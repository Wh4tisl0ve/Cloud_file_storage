import io
import minio

from unittest import TestCase

from .base_test_class import S3ServiceBaseConfigClass


class S3ServiceFilesTestCase(S3ServiceBaseConfigClass, TestCase):
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

    def test_create_exists_file(self):
        # Test case: Create exists file
        user_id = 1
        directory_name = "test"
        object_name = "test.txt"

        self.s3_service.create_object(
            user_id,
            object_name=object_name,
            current_directory=directory_name,
            data=io.BytesIO(b"test"),
        )

        with self.assertRaises(Exception):
            self.s3_service.create_object(
                user_id,
                object_name=object_name,
                current_directory=directory_name,
                data=io.BytesIO(b"test"),
            )

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
