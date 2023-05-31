import os
import firebase_admin
from dotenv import dotenv_values
from firebase_admin import credentials
from google.cloud import storage
from google.oauth2 import service_account

class Config:
    def __init__(self):
        self.api_key = get_api_key()
        self.firebase_app = get_firebase_instance()
        self.project_id = get_project_id()
        self.gcs_app = get_gcs(self.project_id)


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
    storage_credentials = service_account.Credentials.from_service_account_file("service_gcp.json")
    client = storage.Client(project=project_id, credentials=storage_credentials)
    return client
