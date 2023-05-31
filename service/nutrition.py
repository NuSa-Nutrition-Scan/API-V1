from .gcs.storage import Storage
from typing import Any, BinaryIO

class NutritionService:
    def __init__(self, app: Any, storage: Storage):
        self.storage = storage
        self.app = app

    def upload_nutrition_photo(self, file: BinaryIO, user_id: str):
        path = f"{user_id}/photo"
        uploaded_photo_url = self.storage.store(file=file, save_as=path)
        return uploaded_photo_url
