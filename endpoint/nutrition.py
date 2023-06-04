from fastapi import APIRouter, UploadFile, Depends
from .security import extract_token, User
from service.nutrition import NutritionService

def routes(service: NutritionService) -> APIRouter: 
    router = APIRouter(prefix="/nutrition")

    @router.post("/photo")
    async def upload_file(file: UploadFile, user: User = Depends(extract_token)):
        user_id = user.user_id
        result = service.upload_nutrition_photo(file=file.file, user_id=user_id, content_type=file.content_type)
        return result
    
    @router.get("/photo/all")
    async def get_all_photo_nutrition(user: User = Depends(extract_token), page: int = 0):
        user_id = user.user_id
        result = service.get_all_nutrition_photo(user_id=user_id, page=page)
        return result
    return router