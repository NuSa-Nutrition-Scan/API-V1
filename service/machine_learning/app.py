import json
import os
from gradio_client import Client
from typing import Dict, Union


class MLPredictions:
    def __init__(self, food_prediction_api: str):
        self.food_predict_client = Client(food_prediction_api)

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
