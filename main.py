import metadata
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from customizer import validation_body_exception_handler, http_customize_handler
from endpoint.auth import routes as auth_routes
from endpoint.nutrition import routes as nutrition_routes
from endpoint.settings import routes as settings_routes
from service.authentication import AuthService
from service.nutrition import NutritionService
from service.settings import SettingsService
from config import Config

config = Config()

# service
auth_service = AuthService(app=config.firebase_app, api_key=config.api_key)
nutrition_service = NutritionService(
    app=config.firebase_app, storage=config.storage, db=config.firestore_app)
settings_service = SettingsService(app=config.firebase_app, storage=config.storage,
                                   db=config.firestore_app, api_key=config.api_key, auth_service=auth_service)

# router
app = FastAPI(
    title=metadata.title,
    description=metadata.description,
    version=metadata.version,
    contact=metadata.contact,
    license_info=metadata.license_info,
    openapi_tags=metadata.tags_metadata,
    debug=True
)

validation_body_exception_handler(app)
http_customize_handler(app)

app.include_router(auth_routes(auth_service))
app.include_router(nutrition_routes(nutrition_service))
app.include_router(settings_routes(settings_service))


@app.get("/")
async def index() -> JSONResponse:
    return JSONResponse(status_code=200, content={"code": 200, "msg": "OK"})
