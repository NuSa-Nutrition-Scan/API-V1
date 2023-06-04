from fastapi import APIRouter, UploadFile, File, Depends, Form
from fastapi.responses import JSONResponse
from .security import extract_token, User
from service.settings import SettingsService
from typing import Annotated


def routes(service: SettingsService) -> APIRouter:
    router = APIRouter(prefix="/settings")

    @router.patch("/profile/update")
    async def update_profile(
        name: Annotated[str, Form()], 
        refresh_token: Annotated[str, Form()],
        img: UploadFile = File(None), 
        user: User = Depends(extract_token),
        ) -> JSONResponse:    
        if img is not None:
            result = service.update_profile(
                name=name, file=img.file, content_type=img.content_type, user=user, refresh_token=refresh_token)
            return JSONResponse(status_code=result["code"], content=result)

        result = service.update_profile(
            user=user, name=name, file=None, content_type='', refresh_token=refresh_token)
        return JSONResponse(status_code=result["code"], content=result)

    @router.get("/nutrition-photo/all")
    async def get_all_photo_nutrition(user: User = Depends(extract_token), page: int = 0):
        user_id = user.user_id
        result = service.get_upload_nutrition_photo_history(
            user_id=user_id, page=page)
        return JSONResponse(status_code=result["code"], content=result)

    return router
