import firebase_admin
from firebase_admin import credentials
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from customizer import validation_body_exception_handler, http_customize_handler
from endpoint.auth import routes as auth_routes

cred = credentials.Certificate("serviceAccountKey.json")
fb = firebase_admin.initialize_app(credential=cred)

app = FastAPI()
validation_body_exception_handler(app)
http_customize_handler(app)

app.include_router(auth_routes())


@app.get("/")
async def index():
    return JSONResponse(status_code=200, content={"code": 200, "msg": "OK"})
