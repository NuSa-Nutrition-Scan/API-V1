import json
from typing import Any, BinaryIO, Optional

from firebase_admin import auth
from fastapi import HTTPException

from . import result
from .authentication import AuthService
from .gcp.firestore import Firestore
from .gcp.storage import Storage

from collections import ChainMap

DEFAULT_PHOTO_URL = "https://static.vecteezy.com/system/resources/thumbnails/004/511/281/small/default-avatar-photo-placeholder-profile-picture-vector.jpg"


class SettingsService:
    def __init__(
        self,
        app: Any,
        storage: Storage,
        db: Firestore,
        api_key: str,
        auth_service: AuthService,
    ):
        self.storage = storage
        self.app = app
        self.db = db
        self.api_key = api_key
        self.auth_service = auth_service

    def update_profile(
        self,
        name: str,
        file: Optional[BinaryIO],
        content_type: str,
        user: Any,
        weight: int, 
        height: int, 
        sex: str, 
        calories_target: int, 
        age: int, 
        refresh_token: str,
    ):
        if not self.db.is_user_exists(user.user_id):
            raise HTTPException(status_code=401, detail="Unauthorized")
    
        if sex not in ['M', 'F']:
            return result.BadInput({"sex": "Gender can only be male or female"})

        uploaded_photo_url = ""

        if file is not None:
            if user.photo_url != "":
                photo_id = user.photo_url.split("/")[-1]
                path = f"{user.user_id}/profile"

                self.storage.destruct(path=path, photo_id=photo_id)
                uploaded_photo_url = self.storage.store(
                    path=path, file=file, content_type=content_type
                )
            else:
                path = f"{user.user_id}/profile"
                uploaded_photo_url = self.storage.store(
                    path=path, file=file, content_type=content_type
                )

        try:
            if uploaded_photo_url == "":
                auth.update_user(
                    uid=user.user_id,
                    display_name=name,
                )

            else:
                auth.update_user(
                    uid=user.user_id, display_name=name, photo_url=uploaded_photo_url
                )
        except ValueError:
            if uploaded_photo_url != "":
                self.storage.destruct(path=path, photo_id=photo_id)

            return result.Err(code=400, msg="Invalid user")

        except Exception as e:
            print("SettingsService.update_profile:", e)
            if uploaded_photo_url != "":
                self.storage.destruct(path=path, photo_id=photo_id)

            return result.InternalErr()

        updated_data = self.db.save_user_detail(
            weight=weight,
            height=height,
            sex=sex,
            calories_target=calories_target,
            age=age,
            user_id=user.user_id,
        )

        if updated_data is None:
            print("gabisa update data")
            return result.InternalErr()

        token = self.auth_service.refresh_token(refresh_token=refresh_token)

        resp = {
            "id": token["data"]["id"],
            "email": user.email,
            "name": name,
            "photo_url": uploaded_photo_url,
            "token": token["data"]["token"],
            "refresh_token": token["data"]["refresh_token"],
            "expires_in": token["data"]["expires_in"],
        }

        updated_result = dict(ChainMap(resp, updated_data))

        return result.OK(data=updated_result)

    def get_upload_nutrition_photo_history(self, user_id: str, page: int = 0):
        paginated_photos = self.db.get_all_user_nutrition_photo(
            user_id=user_id, skip=page
        )
        return result.OK(data=paginated_photos)

    def _extract_response_text(self, data: Any, key: str) -> str:
        data = json.loads(data)
        return data["error"][key]

    def _get_error_msg_by_firebase_err(self, msg: str) -> str:
        if ("INVALID_ID_TOKEN" in msg) or ("USER_NOT_FOUND" in msg):
            return "Unknown user"

        if "TOKEN_EXPIRED" in msg:
            return "Session has expired. Please sign in again"

        print("service.settings._get_error_msg_by_firebase_err: ", msg)
        return "Bad credentials"
