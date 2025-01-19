from .s3_service import S3Service
from .s3_client import get_minio_client


class S3ServiceFactory:
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        secure: bool = False,
    ):
        self.__endpoint = endpoint
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__secure = secure

    def get_service(self, bucket_name: str) -> S3Service:
        client = get_minio_client(
            self.__endpoint, self.__access_key, self.__secret_key, self.__secure
        )
        return S3Service(client, bucket_name)
