from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse

from service.settings import SettingsService

from .security import User, extract_token


def routes(service: SettingsService) -> APIRouter:
    router = APIRouter(prefix="/settings", tags=["Settings"])

    @router.patch("/profile/update")
    async def update_profile(
        name: Annotated[str, Form()],
        weight: Annotated[int, Form()],
        height: Annotated[int, Form()],
        sex: Annotated[str, Form()],
        calories_target: Annotated[int, Form()],
        age: Annotated[int, Form()],
        refresh_token: Annotated[str, Form()],
        img: UploadFile = File(None),
        user: User = Depends(extract_token),
    ) -> JSONResponse:
        """
        In register, user cannot upload their coolest photo 🥶🥶. \n
        Upload their photo (optional) or change name using this endpoint. \n
        **NOTE:** Requires a Bearer Token \n
        **NOTE #2:** Make sure you send the request in multipart/form-data, not application/json. \n
        **SIDE NOTE:** Also upload the refresh token, because the new token will contains the updated data. \n
        **ANOTHER NOTE:** Remove the current token & current refresh token with the new incoming token & refresh token.

        Response: 200
        ```
        {
            "code": 200,
            "msg": "OK",
            "data": {
                "weight": 80,
                "sex": "M",
                "calories_target": 2200,
                "height": 170,
                "age": 40,
                "id": "vv60n7NvElPdS67LjUab0atAqTO2",
                "email": "mamang@gmail.com",
                "name": "Sambo",
                "photo_url": "https://storage.googleapis.com/nusa-bucket/vv60n7NvElPdS67LjUab0atAqTO2/profile/Jz5MAYdCKMqJUCVSXn38ut",
                "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjY3YmFiYWFiYTEwNWFkZDZiM2ZiYjlmZjNmZjVmZTNkY2E0Y2VkYTEiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiU2FtYm8iLCJwaWN0dXJlIjoiaHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL251c2EtYnVja2V0L3Z2NjBuN052RWxQZFM2N0xqVWFiMGF0QXFUTzIvcHJvZmlsZS9KejVNQVlkQ0tNcUpVQ1ZTWG4zOHV0IiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2N1a2ktNTU3M2YiLCJhdWQiOiJjdWtpLTU1NzNmIiwiYXV0aF90aW1lIjoxNjg2NjY2MDg3LCJ1c2VyX2lkIjoidnY2MG43TnZFbFBkUzY3TGpVYWIwYXRBcVRPMiIsInN1YiI6InZ2NjBuN052RWxQZFM2N0xqVWFiMGF0QXFUTzIiLCJpYXQiOjE2ODY2NjYxNzgsImV4cCI6MTY4NjY2OTc3OCwiZW1haWwiOiJtYW1hbmdAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsibWFtYW5nQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.Bpzg8RAQxBHhMYrG8jL4fhq75tHBpA8TxHGpac6-u_gQzOQ898pW0nb-FuW8d3fqR-9lqs5rbK-b5gQ8tQl4W_I6-xhcDgxIC6BeyyGH_mMIb2oiZrkmZ0cHxUJX6kullQo8U6kzk4FYjDDxvYIudfr55t9rhjyOQqKnFApCJ-XapB1kjgVHVnm0YlKGTPoIksn0G7GAZdUf0uANw66UO4k9sXXDV0LwAqqptH88_f3T7PEyTrFn6JxFPolb6JoDvYOYgIzczeCVNMssLIDxXnJwcBacQI6_amuZB8YK07xxG3exVJNbRkHWd5yrf_5z_AB12g5OjwrqD8r_5KvTEw",
                "refresh_token": "APZUo0QsF4hB9QJrgAwNb1JHUK_jvm57-u0qhwmSKDHZBMbYL7nxnHPdmItH_u1VrXGFqI_nRlS9y6Rpgh3589RKPnC-Xza8YsqFoU-yQkZK2suxfENktaW61gSraihL0G5ako637PGCFkG3-X7vwcP5QwXsyVBz0FZvnUepG-7nZp7FQORp7CnVsWBO_n32hDQzT-B1kXswaq1fFt2QVJGPpG16_MVX6g",
                "expires_in": "3600"
            }
        }
        ```
        """
        if img is not None:
            result = service.update_profile(
                name=name,
                file=img.file,
                content_type=img.content_type,
                user=user,
                refresh_token=refresh_token,
                weight=weight,
                height=height,
                sex=sex,
                calories_target=calories_target,
                age=age,
            )
            return JSONResponse(status_code=result["code"], content=result)

        result = service.update_profile(
            user=user,
            name=name,
            file=None,
            content_type="",
            refresh_token=refresh_token,
            weight=weight,
            height=height,
            sex=sex,
            calories_target=calories_target,
            age=age,
        )
        return JSONResponse(status_code=result["code"], content=result)

    @router.get("/nutrition-photo/all")
    async def get_all_photo_nutrition(
        user: User = Depends(extract_token), page: int = 0
    ):
        """
        Get all the user nutrition photo. \n
        This page will be paginated (means, only first 10 will be given to you, bastard). \n
        **Example:** https://pier.solo.md/settings/nutrition-photo/all?page=0 (fetch first 10 latest photo) \n
        **NOTE:** Requires a Bearer Token \n

        Response: 200
        ```
        {
            "code": 200,
            "msg": "OK",
            "data": [
                {
                    "nutrition_id": "cfQ32yHxGrsLtUJEdtGo",
                    "img_url": "https://storage.googleapis.com/nusa-bucket/lrGpw03KXZTy7ZW9Um2OO1Bxxr72/nutrition/QRe65L5QFTc8mafSGmPJeb",
                    "user_id": "lrGpw03KXZTy7ZW9Um2OO1Bxxr72",
                    "created_at": "2023-06-07 19:16:31"
                },
                {
                    "nutrition_id": "cfQ32yHxGrsLtUJEdtGo",
                    "img_url": "https://storage.googleapis.com/nusa-bucket/lrGpw03KXZTy7ZW9Um2OO1Bxxr72/nutrition/QRe65L5QFTc8mafSGmPJeb",
                    "user_id": "lrGpw03KXZTy7ZW9Um2OO1Bxxr72",
                    "created_at": "2023-06-07 19:18:31"
                },
                {
                    "nutrition_id": "cfQ32yHxGrsLtUJEdtGo",
                    "img_url": "https://storage.googleapis.com/nusa-bucket/lrGpw03KXZTy7ZW9Um2OO1Bxxr72/nutrition/QRe65L5QFTc8mafSGmPJeb",
                    "user_id": "lrGpw03KXZTy7ZW9Um2OO1Bxxr72",
                    "created_at": "2023-06-07 19:16:31"
                },
                {
                    "nutrition_id": "cfQ32yHxGrsLtUJEdtGo",
                    "img_url": "https://storage.googleapis.com/nusa-bucket/lrGpw03KXZTy7ZW9Um2OO1Bxxr72/nutrition/QRe65L5QFTc8mafSGmPJeb",
                    "user_id": "lrGpw03KXZTy7ZW9Um2OO1Bxxr72",
                    "created_at": "2023-06-07 19:18:31"
                },
                {
                    "nutrition_id": "cfQ32yHxGrsLtUJEdtGo",
                    "img_url": "https://storage.googleapis.com/nusa-bucket/lrGpw03KXZTy7ZW9Um2OO1Bxxr72/nutrition/QRe65L5QFTc8mafSGmPJeb",
                    "user_id": "lrGpw03KXZTy7ZW9Um2OO1Bxxr72",
                    "created_at": "2023-06-07 19:16:31"
                },
                {
                    "nutrition_id": "cfQ32yHxGrsLtUJEdtGo",
                    "img_url": "https://storage.googleapis.com/nusa-bucket/lrGpw03KXZTy7ZW9Um2OO1Bxxr72/nutrition/QRe65L5QFTc8mafSGmPJeb",
                    "user_id": "lrGpw03KXZTy7ZW9Um2OO1Bxxr72",
                    "created_at": "2023-06-07 19:18:31"
                }
            ]
        }
        ```
        """
        user_id = user.user_id
        result = service.get_upload_nutrition_photo_history(user_id=user_id, page=page)
        return JSONResponse(status_code=result["code"], content=result)

    return router
