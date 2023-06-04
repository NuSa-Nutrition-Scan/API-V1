from fastapi import FastAPI
from fastapi.responses import JSONResponse
from customizer import validation_body_exception_handler, http_customize_handler
from endpoint.auth import routes as auth_routes
from endpoint.nutrition import routes as nutrition_routes
from service.authentication import AuthService
from service.nutrition import NutritionService
from config import Config
from service.gcp.storage import Storage 

config = Config()

# service
auth_service = AuthService(app=config.firebase_app, api_key=config.api_key)
nutrition_service = NutritionService(app=config.firebase_app, storage=config.storage, db=config.firestore_app)

# router
app = FastAPI()
validation_body_exception_handler(app)
http_customize_handler(app)

app.include_router(auth_routes(auth_service))
app.include_router(nutrition_routes(nutrition_service))

@app.get("/")
async def index() -> JSONResponse:
    return JSONResponse(status_code=200, content={"code": 200, "msg": "OK"})
