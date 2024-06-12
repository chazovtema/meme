from typing import Protocol
from abc import abstractmethod

from io import BytesIO
from minio import Minio  # type: ignore


class FileStorage(Protocol):
    @abstractmethod
    def upload_file(self, file_name: str, data: bytes) -> None: ...

    @abstractmethod
    def get_file(self, file_name: str) -> bytes: ...

    @abstractmethod
    def delete_file(self, file_name: str) -> None: ...


class MinioStorage(FileStorage):
    def __init__(
        self, host: str, user_name: str, password: str, bucket_name: str
    ) -> None:
        self.__bucket = bucket_name
        self.client = Minio(
            endpoint=host, access_key=user_name, secret_key=password, secure=False
        )
        if not self.client.bucket_exists(self.__bucket):
            self.client.make_bucket(self.__bucket)

    def upload_file(self, file_name: str, data: bytes) -> None:
        self.client.put_object(self.__bucket, file_name, BytesIO(data), len(data))

    def get_file(self, file_name: str) -> bytes:
        resp = self.client.get_object(self.__bucket, file_name)
        return resp.data

    def delete_file(self, file_name: str) -> None:
        self.client.remove_object(self.__bucket, file_name)
