import json
import os
from gradio_client import Client
from typing import Dict, Union


class MLPredictions:
    def __init__(self, food_prediction_api: str, food_recomendation_api: str):
        self.food_predict_client = Client(food_prediction_api)
        self.food_recomendation_client = Client(food_recomendation_api)

    def predict_food(self, image_url: str) -> Dict[str, Union[str, list]]:
        job = self.food_predict_client.predict(image_url, api_name="/predict")

        with open(job, "r") as f:
            data_dict = json.load(f)

        final_result: str = data_dict["label"]
        other_options: list = [
            item["label"]
            for item in data_dict["confidences"]
            if item["label"] != final_result
        ]

        output_dict = {"final_result": final_result, "other_options": other_options}

        os.remove(job)
        return output_dict

    def predict_recommendation_food(
        self,
        uid: str,
        age: int,
        weight: int,
        height: int,
        calories_need: int,
        gender: str,
        amount_of_eat_every_day: int,
    ):
        job = self.food_recomendation_client(
            uid, age, weight, height, calories_need, gender, amount_of_eat_every_day
        )
