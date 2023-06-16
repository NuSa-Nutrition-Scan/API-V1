import json
from typing import Any

import requests
from firebase_admin import auth
from firebase_admin._auth_utils import EmailAlreadyExistsError
from firebase_admin.exceptions import FirebaseError

from .gcp.firestore import Firestore

from collections import ChainMap
from . import result

DEFAULT_PHOTO_URL = "https://static.vecteezy.com/system/resources/thumbnails/004/511/281/small/default-avatar-photo-placeholder-profile-picture-vector.jpg"


class AuthService:
    def __init__(self, app: Any, api_key: str, db: Firestore):
        self.app = app
        self.api_key = api_key
        self.db = db

    def create_user(self, name: str, email: str, password: str) -> result.Result:
        try:
            user = auth.create_user(
                app=self.app,
                display_name=name,
                email=email,
                email_verified=True,
                password=password,
            )

            self.db.init_user_detail(user.uid)
            self.db.init_user_scan_count(user.uid)

            return result.Created()

        except EmailAlreadyExistsError:
            return result.Err(400, "Email already exists")

        except FirebaseError as e:
            print(e)
            return result.Err(500, "Can't create user. Try again later")

        except ValueError as e:
            return result.Err(400, str(e))

        except Exception as e:
            print("AuthService.create_user:", e)
            return result.InternalErr()

    def authenticate_user(self, email: str, password: str) -> result.Result:
        request_ref = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"
        headers = {"content-type": "application/json; charset=UTF-8"}

        data = json.dumps(
            {"email": email, "password": password, "returnSecureToken": True}
        )

        try:
            response = requests.post(request_ref, headers=headers, data=data)
            response.raise_for_status()

            obj = response.json()

            resp = {
                "id": obj["localId"],
                "email": obj["email"],
                "name": obj["displayName"],
                "token": obj["idToken"],
                "refresh_token": obj["refreshToken"],
                "expires_in": obj["expiresIn"],
            }

            creds = self.db.get_user_detail(obj["localId"])
            response = dict(ChainMap(resp, creds))

            return result.OK(response)
        except requests.exceptions.HTTPError as e:
            code = e.response.status_code
            txt = self._extract_response_text(e.response.text, "message")
            msg = self._get_error_msg_by_firebase_err(txt)

            return result.Err(code, msg)

        except Exception as e:
            print("AuthService.authenticate_user:", e)
            return result.InternalErr()

    def revoke_token(self, id_user: str) -> result.Result:
        try:
            auth.revoke_refresh_tokens(uid=id_user, app=self.app)
            return result.OK()

        except ValueError:
            return result.Err(400, "Bad credentials")

        except Exception as e:
            print("AuthService.revoke_token:", e)
            return result.InternalErr()

    def refresh_token(self, refresh_token: str) -> result.Result:
        request_ref = f"https://securetoken.googleapis.com/v1/token?key={self.api_key}"
        headers = {"content-type": "application/json; charset=UTF-8"}

        data = json.dumps({"grantType": "refresh_token", "refreshToken": refresh_token})

        try:
            response = requests.post(request_ref, headers=headers, data=data)
            response.raise_for_status()

            obj = response.json()

            resp = {
                "id": obj["user_id"],
                "token": obj["id_token"],
                "refresh_token": obj["refresh_token"],
                "expires_in": obj["expires_in"],
            }

            return result.OK(resp)

        except requests.exceptions.HTTPError as e:
            code = e.response.status_code
            txt = self._extract_response_text(e.response.text, "message")
            msg = self._get_error_msg_by_firebase_err(txt)

            return result.Err(code, msg)

        except Exception as e:
            print("AuthService.refresh_token:", e)
            return result.InternalErr()

    def who_am_i(self, user):
        creds = self.db.get_user_detail(user.user_id)
        if creds is None:
            print("user is none")
            return result.InternalErr()

        resp = {
            "id": user.user_id,
            "name": user.name,
            "email": user.email,
            "photo_url": user.photo_url,
        }

        combined_resp = dict(ChainMap(resp, creds))
        return result.OK(combined_resp)

    def _extract_response_text(self, data: Any, key: str) -> str:
        data = json.loads(data)
        return data["error"][key]

    def _get_error_msg_by_firebase_err(self, msg: str) -> str:
        # authentication
        if "EMAIL_NOT_FOUND" in msg:
            return "Unknown user"

        if "INVALID_PASSWORD" in msg:
            return "Bad credentials"

        if "USER_DISABLED" in msg:
            return "Unknown user"

        if "TOO_MANY_ATTEMPT" in msg:
            return "Too many attempt. Please try again later"

        # refresh token
        if "TOKEN_EXPIRED" in msg:
            return "Session has expired. Please sign in again"

        if ("USER_DISABLED" in msg) or ("USER_NOT_FOUND" in msg):
            return "Unknown user"

        if ("INVALID_REFRESH_TOKEN" in msg) or ("MISSING_REFRESH_TOKEN" in msg):
            return "Bad credentials"

        print(msg)
        return "Bad credentials"
