from minio import Minio


def get_minio_client(
    endpoint: str, access_key: str, secret_key: str, secure: bool = False
) -> Minio:
    return Minio(
        endpoint=endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=secure,
    )
