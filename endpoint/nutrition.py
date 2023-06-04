from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import JSONResponse
from .security import extract_token, User
from service.nutrition import NutritionService

def routes(service: NutritionService) -> APIRouter: 
    router = APIRouter(prefix="/nutrition")

    @router.post("/photo")
    async def upload_photo(file: UploadFile, user: User = Depends(extract_token)) -> JSONResponse:
        result = service.upload_nutrition_photo(file=file.file, user_id=user.user_id, content_type=file.content_type)
        return JSONResponse(status_code=result["code"], content=result)

    return router