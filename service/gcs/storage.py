from google.cloud import storage
from google.cloud.storage.bucket import Bucket
from typing import BinaryIO

class Storage:
    def __init__(self, client: storage.Client, bucket_name: str):
        self.bucket_name = bucket_name
        self.bucket: Bucket = client.get_bucket(bucket_name)

    def store(self, file: BinaryIO, save_as: str) -> str:
        blob = self.bucket.blob(save_as)
        blob.upload_from_file(file)
        return f"https://storage.google.cloud.com/{self.bucket_name}/{save_as}"
