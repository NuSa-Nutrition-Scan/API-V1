from typing import Any, BinaryIO

from . import result
from .gcp.firestore import Firestore
from .gcp.storage import Storage
from .machine_learning.app import MLPredictions


class NutritionService:
    def __init__(self, app: Any, storage: Storage, db: Firestore, ml: MLPredictions):
        self.storage = storage
        self.app = app
        self.db = db
        self.ml = ml
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

    def predict_food(self, file: BinaryIO, content_type: str, user_id: str):
        path = f"temp"
        uploaded_photo_url = self.storage.store(
            path=path, file=file, content_type=content_type
        )

        prediction_result = self.ml.predict_food(uploaded_photo_url)
        eat_per_day = self.db.get_user_detail(user_id)["eat_per_day"]
        final_result = self.db.get_food_by_name(prediction_result["final_result"])

        if eat_per_day == 2 or eat_per_day == "2":
            resp = {
                "id": final_result["id"],
                "name": final_result["name"],
                "calories": final_result["calories_for_2x"],
                "karbohidrat": final_result["karbohidrat"],
                "lemak": final_result["lemak"],
                "mineral": final_result["mineral"],
                "protein": final_result["protein"],
                "vitamin": final_result["vitamin"],
            }

            return result.OK(data=resp)

        if eat_per_day == 3 or eat_per_day == "3":
            resp = {
                "id": final_result["id"],
                "name": final_result["name"],
                "calories": final_result["calories_for_3x"],
                "karbohidrat": final_result["karbohidrat"],
                "lemak": final_result["lemak"],
                "mineral": final_result["mineral"],
                "protein": final_result["protein"],
                "vitamin": final_result["vitamin"],
            }

            return result.OK(data=resp)

        resp = {
            "id": final_result["id"],
            "name": final_result["name"],
            "calories": final_result["calories_for_4x"],
            "karbohidrat": final_result["karbohidrat"],
            "lemak": final_result["lemak"],
            "mineral": final_result["mineral"],
            "protein": final_result["protein"],
            "vitamin": final_result["vitamin"],
        }

        return result.OK(data=resp)

    def get_recommendation_food(self, user_id: str):
        user = self.db.get_user_detail(user_id)
        if user["has_been_updated"] is False:
            return result.Err(
                400,
                "Can't generate recommendation. Please fill the data first in the profile.",
            )

        print(user)

        resp = self.db.get_recommendation_food(user_id, user["eat_per_day"])
        if resp is None:
            return result.Err(code=423, msg="Still generating. Please wait")

        return result.OK(data=resp)

    def get_count_photo_today(self, user_id: str):
        count = self.db.get_count_nutrition_input_today(user_id=user_id)

        resp = {"count": count}

        return result.OK(data=resp)
