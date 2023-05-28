import requests
import json
from dotenv import dotenv_values

env = dotenv_values(".env")
api_key = env["API_KEY"]

class Result:
    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data

def signup(email: str, password: str) -> Result:
    request_ref = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    headers = {"content-type": "application/json; charset=UTF-8"}
    
    data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
    request_object = requests.post(request_ref, headers=headers, data=data)
    
    result = Result(request_object.status_code, request_object.json())
    return result

def signin(email: str, password: str) -> Result:
    request_ref = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    headers = {"content-type": "application/json; charset=UTF-8"}
    
    data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
    request_object = requests.post(request_ref, headers=headers, data=data)
    
    result = Result(request_object.status_code, request_object.json())
    return result

def refresh(refresh_token: str) -> Result:
    request_ref = f"https://securetoken.googleapis.com/v1/token?key={api_key}"
    headers = {"content-type": "application/json; charset=UTF-8"}

    data = json.dumps({"grantType": "refresh_token", "refreshToken": refresh_token})
    request_object = requests.post(request_ref, headers=headers, data=data)
    
    request_object_json = request_object.json()

    user = {
        "userId": request_object_json["user_id"],
        "idToken": request_object_json["id_token"],
        "refreshToken": request_object_json["refresh_token"]
    }

    result = Result(request_object.status_code, user)
    return result

def get_user_info(id_token: str) -> Result:
    request_ref = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={api_key}"
    headers = {"content-type": "application/json; charset=UTF-8"}
    
    data = json.dumps({"idToken": id_token})
    request_object = requests.post(request_ref, headers=headers, data=data)
    
    result = Result(request_object.status_code, request_object.json())
    return result


def ban_token(token: str) -> Result:
    result = Result()
    return result