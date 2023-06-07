from fastapi import APIRouter, UploadFile, File, Depends, Form
from fastapi.responses import JSONResponse
from .security import extract_token, User
from service.settings import SettingsService
from typing import Annotated


def routes(service: SettingsService) -> APIRouter:
    router = APIRouter(prefix="/settings", tags=["Settings"])

    @router.patch("/profile/update")
    async def update_profile(
        name: Annotated[str, Form()], 
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
                    "id": "lrGpw03KXZTy7ZW9Um2OO1Bxxr72",
                    "email": "useramboy@gmail.com",
                    "name": "Sundel Bolong",
                    "photo_url": "https://storage.googleapis.com/nusa-bucket/lrGpw03KXZTy7ZW9Um2OO1Bxxr72/profile/XhfwFfYfTSokE5SnyV7VBA",
                    "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU0NWUyNDZjNTEwNmExMGQ2MzFiMTA0M2E3MWJiNTllNWJhMGM5NGQiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiU3VuZGVsIEJvbG9uZyIsInBpY3R1cmUiOiJodHRwczovL3N0b3JhZ2UuZ29vZ2xlYXBpcy5jb20vbnVzYS1idWNrZXQvbHJHcHcwM0tYWlR5N1pXOVVtMk9PMUJ4eHI3Mi9wcm9maWxlL1hoZndGZllmVFNva0U1U255VjdWQkEiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vY3VraS01NTczZiIsImF1ZCI6ImN1a2ktNTU3M2YiLCJhdXRoX3RpbWUiOjE2ODYxNDAwMjQsInVzZXJfaWQiOiJsckdwdzAzS1haVHk3Wlc5VW0yT08xQnh4cjcyIiwic3ViIjoibHJHcHcwM0tYWlR5N1pXOVVtMk9PMUJ4eHI3MiIsImlhdCI6MTY4NjE0MDQ0MiwiZXhwIjoxNjg2MTQ0MDQyLCJlbWFpbCI6InVzZXJhbWJveUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJ1c2VyYW1ib3lAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.sgNYkuE3e5XX2Ko9h1sK3fFcAP_zRzXjdGhnD9ODuoGTAH_5gxESYa64j-MMNQmAgiJdtYpELoWQcDrNfefKWa2U2irHLcTBrLRIFvnVhVLzWfCGB2LfLxgdLtt4VSnJTbGzFZK3QQI_41jxhpFU3LinarRDpUUa6i0Z79IFhoZp-Bk8xVpInuj_zAuXiiNmKdzGb7K7FoFs8FH0BUO3qy2Ik9qIdDZ9yFtnz7vx_SNk50gxCYinVqEf71qoiaGODGhn0n6iU1rSub0tNVjr4j4MImCivtbEsjihUMtq-kNvxNjGMEyyjubpqS_qK5aNYw3aFNSPwAI12O2LlY9law",
                    "refresh_token": "APZUo0SRj1QpmSn459aRsyYbS--tsbXULY_m2MwzSxibx39JzrVgUs7Z2MfrvmPLP_Vm_k-oEk2sUsmu81QA0ReV7rykH9EBXN77nndLr4nEog80rnzfBhxHZDJlXaM-aadN9olBEC3wI0E27ALj287Z9pRq8wi8qKWWbNHLuLxcD29PJgLIsgL4-aEQ2AH11m91P9YYa2zza_PNoNeoFZzknZOgqA6j3A",
                    "expires_in": "3600"
                }
            }
            ```
        """
        if img is not None:
            result = service.update_profile(
                name=name, file=img.file, content_type=img.content_type, user=user, refresh_token=refresh_token)
            return JSONResponse(status_code=result["code"], content=result)

        result = service.update_profile(
            user=user, name=name, file=None, content_type='', refresh_token=refresh_token)
        return JSONResponse(status_code=result["code"], content=result)

    @router.get("/nutrition-photo/all")
    async def get_all_photo_nutrition(user: User = Depends(extract_token), page: int = 0):
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
        result = service.get_upload_nutrition_photo_history(
            user_id=user_id, page=page)
        return JSONResponse(status_code=result["code"], content=result)

    return router
