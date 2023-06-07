from typing import Any, BinaryIO

from . import result
from .gcp.firestore import Firestore
from .gcp.storage import Storage


class NutritionService:
    def __init__(self, app: Any, storage: Storage, db: Firestore):
        self.storage = storage
        self.app = app
        self.db = db
        self.MAX_PHOTO_INPUT = 10

    def upload_nutrition_photo(self, file: BinaryIO, user_id: str, content_type: str):
        user_input = self.db.get_count_nutrition_input_today(user_id=user_id)
        if user_input == self.MAX_PHOTO_INPUT:
            return result.Err(
                code=400,
                msg="You have reached the maximum photo you can upload. Try again tomorrow",
            )

        path = f"{user_id}/nutrition"
        uploaded_photo_url = self.storage.store(
            path=path, file=file, content_type=content_type
        )

        saved_result = self.db.save_nutrition_data(
            user_id=user_id, img_url=uploaded_photo_url
        )

        return result.OK(data=saved_result)

    def get_count_photo_today(self, user_id: str):
        count = self.db.get_count_nutrition_input_today(user_id=user_id)

        resp = {"count": count}

        return result.OK(data=resp)
