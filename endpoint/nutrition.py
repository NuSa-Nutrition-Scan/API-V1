from fastapi import APIRouter, UploadFile, Depends
from .security import extract_token, User
from service.nutrition import NutritionService

def routes(service: NutritionService) -> APIRouter: 
    router = APIRouter(prefix="/nutrition")

    @router.post("/photo")
    async def upload_file(file: UploadFile, user: User = Depends(extract_token)):
        user_id = user.user_id
        result = service.upload_nutrition_photo(file=file.file, user_id=user_id)
        return result
    return router