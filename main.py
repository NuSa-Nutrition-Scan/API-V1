import pkg
from fastapi import FastAPI, Response
from dto import AuthBody, RefreshTokenBody

app = FastAPI()

@app.get("/")
async def index():
    return {"msg": "OK"}

@app.post("/signup")
async def signup(body: AuthBody, response: Response):
    result = pkg.signup(body.email, body.password)
    response.status_code = result.status_code
    return result.data

@app.post("/signin")
async def login(body: AuthBody, response: Response):
    result = pkg.signin(body.email, body.password)
    response.status_code = result.status_code
    return result.data


@app.put("/refresh")
async def refresh(body: RefreshTokenBody, response: Response):
    result = pkg.refresh(body.refresh_token)
    response.status_code = result.status_code
    return result.data

@app.get("/info/{id_token}")
async def refresh(id_token: str, response: Response):
    result = pkg.get_user_info(id_token)
    response.status_code = result.status_code
    return result.data