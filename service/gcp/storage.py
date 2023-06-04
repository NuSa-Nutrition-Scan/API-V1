import shortuuid
from google.cloud import storage
from google.cloud.storage.bucket import Bucket
from typing import BinaryIO

class Storage:
    def __init__(self, client: storage.Client, bucket_name: str):
        self.bucket_name = bucket_name
        self.bucket: Bucket = client.get_bucket(bucket_name)
        self.app_name = "NuSa"

    def store(self, path: str, file: BinaryIO, content_type: str) -> str:
        save_as = self.__id()
        blob = self.bucket.blob(f"{path}/{save_as}")
        blob.upload_from_file(file, content_type=content_type)
        return f"https://storage.googleapis.com/{self.bucket_name}/{save_as}"

    def __id(self) -> str:
        return shortuuid.uuid(name=self.app_name)