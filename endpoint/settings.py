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
        """
        user_id = user.user_id
        result = service.get_upload_nutrition_photo_history(
            user_id=user_id, page=page)
        return JSONResponse(status_code=result["code"], content=result)

    return router
