from typing import BinaryIO

import shortuuid
from fastapi import HTTPException
from google.cloud import storage
from google.cloud.exceptions import NotFound
from google.cloud.storage.bucket import Bucket


class Storage:
    def __init__(self, client: storage.Client, bucket_name: str):
        self.bucket_name = bucket_name
        self.bucket: Bucket = client.get_bucket(bucket_name)

    def store(self, path: str, file: BinaryIO, content_type: str) -> str:
        save_as = self.__id()
        blob = self.bucket.blob(f"{path}/{save_as}")
        blob.upload_from_file(file, content_type=content_type)
        return f"https://storage.googleapis.com/{self.bucket_name}/{path}/{save_as}"

    def destroy(self, path: str, user_id: str):
        try:
            if self.__folder_exists(f"{user_id}/profile"):
                blob = self.bucket.blob(f"{user_id}/profile/{path}")
                print(f"{user_id}/profile/{path}")
                blob.delete()
        except NotFound:
            raise HTTPException(status_code=400, detail="Image not found")
        except Exception as e:
            print("gcp.Storage.destroy:", e)
            raise HTTPException(status_code=500, detail="Internal error")

    def destruct(self, path: str, photo_id: str):
        try:
            if self.__folder_exists(path):
                blob = self.bucket.blob(f"{path}/{photo_id}")
                blob.delete()
        except NotFound:
            raise HTTPException(status_code=400, detail="Image not found")
        except Exception as e:
            print("gcp.Storage.destroy:", e)
            raise HTTPException(status_code=500, detail="Internal error")

    def __id(self) -> str:
        return shortuuid.uuid()

    def __folder_exists(self, path: str) -> bool:
        folder_path = f"{path}/"
        blobs = self.bucket.list_blobs(prefix=folder_path)
        for blob in blobs:
            if path in blob.name:
                return True

        return False
