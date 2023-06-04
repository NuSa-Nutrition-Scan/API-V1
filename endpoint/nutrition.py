from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import JSONResponse
from .security import extract_token, User
from service.nutrition import NutritionService

def routes(service: NutritionService) -> APIRouter: 
    router = APIRouter(prefix="/nutrition", tags=["Nutrition"])

    @router.post("/photo")
    async def upload_photo(file: UploadFile, user: User = Depends(extract_token)) -> JSONResponse:
        """
            Upload a photo (for nutrition). \n
            Example: your food, your beverages, your ex (ಥ _ ಥ). \n
            **NOTE:** Requires a Bearer Token. \n
            **NOTE #2:** Make sure you send the request in multipart/form-data, not application/json
        """
        result = service.upload_nutrition_photo(file=file.file, user_id=user.user_id, content_type=file.content_type)
        return JSONResponse(status_code=result["code"], content=result)

    @router.get('/photo/count')
    async def count_upload_photo(user: User = Depends(extract_token)) -> JSONResponse:
        """
            Every day, a user can only upload photo 10 times a day. \n
            Hit this api, so user can know how many times they upload their photo. \n
            **NOTE:** Requires a Bearer Token \n
        """
        result = service.get_count_photo_today(user_id=user.user_id)
        return JSONResponse(status_code=result["code"], content=result)

    return router