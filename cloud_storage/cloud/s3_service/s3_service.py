import io

import zipfile
from zipfile import ZipFile

import minio
import minio.datatypes

from minio import Minio
from minio.error import S3Error
from minio.deleteobjects import DeleteObject
from minio.commonconfig import CopySource, SnowballObject

from .exceptions import ObjectNameError, ObjectExistsError
from .validators import check_object_name


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
    ) -> None:
        check_object_name(object_name.strip("/"))

        object_path = self.create_path(user_id, object_name, current_directory)

        try:
            self.__client.stat_object(self.__bucket_name, object_path)
            raise ObjectExistsError("Объект с таким именем уже существует")
        except S3Error:
            self.__client.put_object(
                self.__bucket_name,
                object_path,
                data=data,
                length=len(data.getbuffer()),
            )

    def upload_objects(
        self,
        user_id: int,
        files: list,
        current_directory: str = "",
    ) -> None:
        snowball_list = []

        for file in files:
            file_name = file.name.split('/')[-1]
            check_object_name(file_name.strip("/"))
            
            file_data = file.read()

            snowball_list.append(
                SnowballObject(
                    self.create_path(user_id, file.name, current_directory),
                    data=io.BytesIO(file_data),
                    length=len(io.BytesIO(file_data).getbuffer()),
                )
            )

        self.__client.upload_snowball_objects(self.__bucket_name, snowball_list)

    def get_objects(
        self, user_id: str, subdirectory: str = ""
    ) -> list[minio.datatypes.Object]:
        target_path = self.create_path(user_id, directory=subdirectory)

        user_objects = self.__client.list_objects(
            self.__bucket_name, prefix=target_path, start_after=target_path
        )

        objects = [
            minio.datatypes.Object(
                self.__bucket_name,
                object_name=obj.object_name.replace(target_path, ""),
                last_modified=obj.last_modified,
                size=obj.size,
            )
            for obj in user_objects
        ]

        objects.reverse()

        return objects

    def delete_object(
        self, user_id: int, object_name: str, current_directory: str = ""
    ) -> None:
        object_path = self.create_path(user_id, object_name, current_directory)

        if minio.datatypes.Object(self.__bucket_name, object_path).is_dir:
            delete_object_list = map(
                lambda obj: DeleteObject(obj.object_name),
                self.__client.list_objects(
                    self.__bucket_name, recursive=True, prefix=object_path
                ),
            )
            list(self.__client.remove_objects(self.__bucket_name, delete_object_list))
        else:
            self.__client.remove_object(self.__bucket_name, object_path)

    def rename_object(
        self, user_id: int, old_name: str, new_name: str, directory: str = ""
    ) -> None:
        check_object_name(new_name.strip("/"))

        if old_name == new_name:
            raise ObjectNameError("Имена не могут быть одинаковыми")

        new_object = self.create_path(user_id, new_name, directory)

        old_object = self.create_path(user_id, old_name, directory)

        try:
            self.__client.stat_object(self.__bucket_name, new_object)
            raise ObjectExistsError("Объект с таким именем уже существует")
        except S3Error:
            if minio.datatypes.Object(self.__bucket_name, old_object).is_dir:
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
            else:
                self.__client.copy_object(
                    self.__bucket_name,
                    new_object,
                    CopySource(self.__bucket_name, old_object),
                )
                self.__client.remove_object(self.__bucket_name, old_object)

    def get_object_bytes(
        self, user_id: int, object_name: str, current_directory: str = ""
    ) -> io.BytesIO:
        object_path = self.create_path(user_id, object_name, current_directory)

        if minio.datatypes.Object(self.__bucket_name, object_path).is_dir:
            zip_buffer = io.BytesIO()

            object_child = self.__client.list_objects(
                self.__bucket_name, recursive=True, prefix=object_path
            )

            with ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip:
                for object in object_child:
                    current_object_bytes = self.create_object_bytes(object.object_name)

                    object_path_archive = object_path.replace(object_name, "")
                    object_name_archive = object.object_name.replace(
                        object_path_archive, ""
                    )

                    zip.writestr(object_name_archive, current_object_bytes.getvalue())

                object_bytes = zip_buffer
        else:
            object_bytes = self.create_object_bytes(object_path)

        return object_bytes

    def create_object_bytes(self, object_path: str) -> io.BytesIO:
        if minio.datatypes.Object(self.__bucket_name, object_path).is_dir:
            object_bytes = io.BytesIO()
        else:
            response = self.__client.get_object(self.__bucket_name, object_path)
            object_bytes = io.BytesIO(response.read())
            response.close()
            response.release_conn()

        return object_bytes
