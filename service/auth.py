import requests
import json
from .result import Result


class AuthService:
    def __init__(self, api_key, db):
        self.db = db
        self.api_key = api_key

    def signup(self, email: str, password: str) -> Result:
        request_ref = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.api_key}"
        headers = {"content-type": "application/json; charset=UTF-8"}

        data = json.dumps(
            {"email": email, "password": password, "returnSecureToken": True})
        request_object = requests.post(request_ref, headers=headers, data=data)

        result = Result(request_object.status_code, request_object.json())
        return result

    def signin(self, email: str, password: str) -> Result:
        request_ref = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"
        headers = {"content-type": "application/json; charset=UTF-8"}

        data = json.dumps(
            {"email": email, "password": password, "returnSecureToken": True})
        request_object = requests.post(request_ref, headers=headers, data=data)

        result = Result(request_object.status_code, request_object.json())
        return result

    def refresh(self, refresh_token: str) -> Result:
        request_ref = f"https://securetoken.googleapis.com/v1/token?key={self.api_key}"
        headers = {"content-type": "application/json; charset=UTF-8"}

        data = json.dumps({"grantType": "refresh_token",
                          "refreshToken": refresh_token})
        request_object = requests.post(request_ref, headers=headers, data=data)

        request_object_json = request_object.json()

        user = {
            "userId": request_object_json["user_id"],
            "idToken": request_object_json["id_token"],
            "refreshToken": request_object_json["refresh_token"]
        }

        result = Result(request_object.status_code, user)
        return result

    def get_user_info(self, id_token: str) -> Result:
        request_ref = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={self.api_key}"
        headers = {"content-type": "application/json; charset=UTF-8"}

        data = json.dumps({"idToken": id_token})
        request_object = requests.post(request_ref, headers=headers, data=data)

        result = Result(request_object.status_code, request_object.json())
        return result
