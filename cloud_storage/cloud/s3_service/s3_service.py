import io
from typing import Generator

from minio import Minio
from minio.error import S3Error
from minio.commonconfig import CopySource


class S3Service:
    def __init__(self, client: Minio, bucket_name: str):
        self.__client = client
        self.__bucket_name = bucket_name

    def create_path(
        self, user_id: int, object_name: str = "", directory: str = ""
    ) -> str:
        root_directory = f"user-{user_id}-files"

        if directory:
            return f"{root_directory}/{directory}/{object_name}"

        if object_name:
            return f"{root_directory}/{object_name}"

        return f"{root_directory}/"

    def create_object(
        self,
        user_id: int,
        object_name: str,
        current_directory: str = "",
        data: io.BytesIO = io.BytesIO(b""),
    ) -> str:
        data = io.BytesIO(data)
        
        object_path = self.create_path(user_id, object_name, current_directory)

        self.__client.put_object(
            self.__bucket_name,
            object_path,
            data=data,
            length=len(data.getbuffer()),
        )

        return object_path

    def get_objects(self, user_id: str, directory: str) -> Generator:
        target_path = self.create_path(user_id, directory=directory)

        return self.__client.list_objects(self.__bucket_name, prefix=target_path)

    def delete_object(
        self, user_id: int, object_name: str, current_directory: str = ""
    ) -> str:
        object_path = self.create_path(user_id, object_name, current_directory)

        self.__client.remove_object(self.__bucket_name, object_path)

        return object_path

    def rename_object(
        self, user_id: int, old_name: str, new_name: str, directory: str = ""
    ) -> None:
        if old_name == new_name:
            raise Exception("Имена не могут быть одинаковыми")

        new_object = self.create_path(user_id, new_name, directory)

        old_object = self.create_path(user_id, old_name, directory)

        try:
            self.__client.stat_object(self.__bucket_name, new_object)
        except S3Error:
            old_object_child = self.__client.list_objects(
                self.__bucket_name, recursive=True, prefix=old_object
            )
            for object in old_object_child:
                self.__client.copy_object(
                    self.__bucket_name,
                    object.object_name.replace(old_object, new_object),
                    CopySource(self.__bucket_name, object.object_name),
                )
                self.__client.remove_object(self.__bucket_name, object.object_name)
