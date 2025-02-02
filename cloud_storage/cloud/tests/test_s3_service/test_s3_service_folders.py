import io
import minio

from unittest import TestCase

from .base_test_class import S3ServiceBaseConfigClass


class S3ServiceFoldersTestCase(S3ServiceBaseConfigClass, TestCase):
    def test_create_directory(self):
        # Test case: Create empty "directory"
        user_id = 1
        directory_name = "test/"

        self.s3_service.create_object(user_id, object_name=directory_name)
        object_path = self.s3_service.create_path(user_id, directory_name)

        target_object = self.client.stat_object(self.bucket_name, object_path)
        self.assertEqual(object_path, target_object.object_name)

    def test_create_exists_directory(self):
        # Test case: Create exists "directory"
        user_id = 1
        directory_name = "test/"

        self.s3_service.create_object(user_id, object_name=directory_name)

        with self.assertRaises(Exception):
            self.s3_service.create_object(user_id, object_name=directory_name)

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

    def test_delete_nested_directory(self):
        # Test case: Delete nested "directory"
        user_id = 1

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

        all_directories = list(
            self.client.list_objects(
                self.bucket_name, start_after="test/", recursive=True
            )
        )

        self.assertTrue(all_directories)

        self.s3_service.delete_object(user_id, "test/")

        all_directories = list(
            self.client.list_objects(
                self.bucket_name, start_after="test/", recursive=True
            )
        )

        self.assertFalse(all_directories)

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

    def test_find_folders(self):
        user_id = 1
        query_string = "es"

        for i in range(5):
            self.s3_service.create_object(user_id, object_name=f"test{i}/")

        self.s3_service.create_object(
            user_id, object_name="Yes/", current_directory="folder"
        )

        objects = self.s3_service.find_objects(user_id, query_string)

        for obj in objects:
            self.assertIn(query_string, obj.object_name.rstrip("/").split("/")[-1])
