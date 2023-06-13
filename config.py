import os

import firebase_admin
from dotenv import dotenv_values
from firebase_admin import credentials, firestore
from google.cloud import storage
from google.oauth2 import service_account

from service.gcp.firestore import Firestore
from service.gcp.storage import Storage
from service.machine_learning.app import MLPredictions


class Config:
    def __init__(self):
        self.api_key = get_api_key()
        self.firebase_app = get_firebase_instance()
        self.project_id = get_project_id()
        self.gcs_app = get_gcs(self.project_id)
        self.bucket_name = get_bucket_name()
        self.storage = Storage(client=self.gcs_app, bucket_name=self.bucket_name)
        self.firestore_app = get_firestore(self.firebase_app)
        self.ml = get_machine_learning_instance()


def get_api_key() -> str:
    try:
        api_key = os.getenv("API_KEY")
        if api_key is not None:
            return api_key

        raise ValueError
    except ValueError:
        env = dotenv_values(".env")
        api_key = env["API_KEY"]
        if api_key is not None:
            return api_key
        raise Exception
    except Exception:
        print("API_KEY is none")
        exit(1)


def get_firebase_instance():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(credential=cred)
    fb_instance = firebase_admin.get_app()
    return fb_instance


def get_project_id() -> str:
    try:
        project_id = os.getenv("PROJECT_ID")
        if project_id is not None:
            return project_id

        raise ValueError
    except ValueError:
        env = dotenv_values(".env")
        project_id = env["PROJECT_ID"]
        if project_id is None:
            raise Exception
    except Exception:
        print("PROJECT_ID is none")
        exit(1)


def get_bucket_name():
    try:
        bucket_name = os.getenv("BUCKET_NAME")
        if bucket_name is not None:
            return bucket_name

        raise ValueError
    except ValueError:
        env = dotenv_values(".env")
        bucket_name = env["BUCKET_NAME"]
        if bucket_name is not None:
            return bucket_name

        raise Exception
    except Exception:
        print("BUCKET_NAME is none")
        exit(1)


def get_gcs(project_id: str) -> storage.Client:
    storage_credentials = service_account.Credentials.from_service_account_file(
        "service_gcp.json"
    )
    client = storage.Client(project=project_id, credentials=storage_credentials)
    return client


def get_firestore(firebase_app):
    client = firestore.client(app=firebase_app)
    return Firestore(db=client)


def get_machine_learning_instance() -> MLPredictions:
    try:
        food_predict_url = os.getenv("FOOD_PREDICTIONS_API")
        food_recommendation_url = os.getenv("FOOD_PREDICTIONS_API")
        if food_predict_url is not None and food_recommendation_url is not None:
            ml = MLPredictions(
                food_prediction_api=food_predict_url,
                food_recomendation_api=food_recommendation_url,
            )
            return ml

        raise ValueError

    except ValueError:
        env = dotenv_values(".env")
        food_predict_url = env["FOOD_PREDICTIONS_API"]
        food_recommendation_url = env["FOOD_PREDICTIONS_API"]
        if food_predict_url is not None and food_recommendation_url is not None:
            ml = MLPredictions(
                food_prediction_api=food_predict_url,
                food_recomendation_api=food_recommendation_url,
            )
            return ml

        raise Exception

    except Exception:
        print("Machine Learning Instance creds is empty.")
        exit(1)
