from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import JSONResponse

from service.nutrition import NutritionService

from .security import User, extract_token


def routes(service: NutritionService) -> APIRouter:
    router = APIRouter(prefix="/nutrition", tags=["Nutrition"])

    @router.get("/recommendation")
    async def get_recommendation_food_for_user(
        user: User = Depends(extract_token),
    ) -> JSONResponse:
        """
        Get user recommendation food.\n
        If still generating? Response 423 will be thrown.\n

        Response: 423
        ```
        {
            "code": 423,
            "msg": "Still generating. Please wait"
        }
        ```

        <br/>

        All Responses (Notice the "recom" part)

        Response: 200 (if eat times per day is 2)
        ```
        {
            "code": 200,
            "msg": "OK",
            "data": {
                "top15": [
                    {
                        "id": "FNT151",
                        "name": "Singkong Goreng"
                    },
                    {
                        "id": "FNT040",
                        "name": "Ketupat kandangan"
                    },
                    {
                        "id": "FNT010",
                        "name": "Sop konro"
                    },
                    {
                        "id": "FNT024",
                        "name": "Kembang tahu rebus"
                    },
                    //until 15 data
                ],
                "recom": [
                    {
                        "Lunch": "Mi Goreng",
                        "Dinner": "Biskuit"
                    },
                    {
                        "Lunch": "Daging sapi kornet",
                        "Dinner": "Mi Goreng"
                    },
                    {
                        "Lunch": "Daging sapi kornet",
                        "Dinner": "Biskuit"
                    },
                   //until 20 data
                ]
            }
        }
        ```

        Response: 200 (if eat times per day is 3)
        ```
        {
            "code": 200,
            "msg": "OK",
            "data": {
                "top15": [
                    {
                        "id": "FNT151",
                        "name": "Singkong Goreng"
                    },
                    {
                        "id": "FNT040",
                        "name": "Ketupat kandangan"
                    },
                    {
                        "id": "FNT010",
                        "name": "Sop konro"
                    },
                    {
                        "id": "FNT024",
                        "name": "Kembang tahu rebus"
                    },
                    //until 15 data
                ],
                "recom": [
                    {
                        "Lunch": "Mi Goreng",
                        "Breakfast": "Daging sapi kornet",
                        "Dinner": "Biskuit"
                    },
                    {
                        "Lunch": "Biskuit",
                        "Breakfast": "Mi Goreng",
                        "Dinner": "Martabak Mesir"
                    },
                    {
                        "Lunch": "Biskuit",
                        "Breakfast": "Mi Goreng",
                        "Dinner": "Roti putih"
                    },
                   //until 20 data
                ]
            }
        }
        ```

        Response: 200 (if eat times per day is 4)
        ```
        {
            "code": 200,
            "msg": "OK",
            "data": {
                "top15": [
                    {
                        "id": "FNT151",
                        "name": "Singkong Goreng"
                    },
                    {
                        "id": "FNT040",
                        "name": "Ketupat kandangan"
                    },
                    {
                        "id": "FNT010",
                        "name": "Sop konro"
                    },
                    {
                        "id": "FNT024",
                        "name": "Kembang tahu rebus"
                    },
                    //until 15 data
                ],
                "recom": [
                    {
                        "Snacks": "Biskuit",
                        "Lunch": "Mi Goreng",
                        "Breakfast": "Daging sapi kornet",
                        "Dinner": "Biskuit"
                    },
                    {
                        "Snacks": "Sate",
                        "Lunch": "Biskuit",
                        "Breakfast": "Mi Goreng",
                        "Dinner": "Martabak Mesir"
                    },
                    {
                        "Snacks": "Nasi",
                        "Lunch": "Biskuit",
                        "Breakfast": "Mi Goreng",
                        "Dinner": "Roti putih"
                    },
                   //until 20 data
                ]
            }
        }
        ```
        """

        result = service.get_recommendation_food(user.user_id)
        return JSONResponse(status_code=result["code"], content=result)

    @router.post("/photo")
    async def upload_photo(
        file: UploadFile, user: User = Depends(extract_token)
    ) -> JSONResponse:
        """
        Upload a photo (for nutrition). \n
        Example: your food, your beverages, your ex (ಥ _ ಥ). \n
        **NOTE:** Requires a Bearer Token. \n
        **NOTE #2:** Make sure you send the request in multipart/form-data, not application/json

        Response: 200
        ```
        {
            "code": 200,
            "msg": "OK",
            "data": {
                "user_id": "lrGpw03KXZTy7ZW9Um2OO1Bxxr72",
                "img_url": "https://storage.googleapis.com/nusa-bucket/lrGpw03KXZTy7ZW9Um2OO1Bxxr72/nutrition/QRe65L5QFTc8mafSGmPJeb",
                "created_at": "2023-06-07 19:15:31"
            }
        }
        ```
        """
        result = service.upload_nutrition_photo(
            file=file.file, user_id=user.user_id, content_type=file.content_type
        )
        return JSONResponse(status_code=result["code"], content=result)

    @router.post("/photo/predict_food", deprecated=True)
    async def predict_food_photo_public(file: UploadFile) -> JSONResponse:
        """
        **NOTE:** THIS IS FOR DEBUGGING PURPOSE. WE HIGHLY ENCOURAGED TO USE THE `predict_food_secure` ROUTES FOR SECURITY. \n

        Give me your photo, and i will predict what kind of food of that photo.\n
        The explanation of the result: \n
        1. final_result: we are very confident this is the result\n
        2. other_options: other 2 results, that maybe also the result\n

        Response: 200
        ```
        {
            "code": 200,
            "msg": "OK",
            "data": {
                "id": "FNT004",
                "name": "Sate",
                "calories": 607
            }
        }
        ```
        """
        result = service.predict_food(file=file.file, content_type=file.content_type)
        return JSONResponse(status_code=result["code"], content=result)

    @router.post("/photo/predict_food_secure")
    async def predict_food_photo_secure(
        file: UploadFile, user: User = Depends(extract_token)
    ) -> JSONResponse:
        """
        📑 _API security is like giving your sensitive data to a toddler and hoping they won't accidentally share it with the world. - Anonymous_ \n

        Give me your photo, and i will predict what kind of food of that photo.\n
        The explanation of the result: \n
        1. final_result: we are very confident this is the result\n
        2. other_options: other 2 results, that maybe also the result\n

        Response: 200
        ```
        {
            "code": 200,
            "msg": "OK",
            "data": {
                "id": "FNT004",
                "name": "Sate",
                "calories": 607
            }
        }
        ```
        """
        result = service.predict_food(
            file=file.file, content_type=file.content_type, user_id=user.user_id
        )
        return JSONResponse(status_code=result["code"], content=result)

    @router.get("/photo/count")
    async def count_upload_photo(user: User = Depends(extract_token)) -> JSONResponse:
        """
        Every day, a user can only upload photo 10 times a day. \n
        Hit this api, so user can know how many times they upload their photo. \n
        **NOTE:** Requires a Bearer Token \n

        Response: 200
        ```
        {
            "code": 200,
            "msg": "OK",
            "data": {
                "count": 1
            }
        }
        ```
        """
        result = service.get_count_photo_today(user_id=user.user_id)
        return JSONResponse(status_code=result["code"], content=result)

    return router
