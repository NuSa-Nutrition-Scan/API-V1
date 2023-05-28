from .dto import SignUpDTO, SignInDTO
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from service.authentication import AuthService
from .deps import extract_token, User

def routes() -> APIRouter:
    router = APIRouter(prefix='/auth')
    service = AuthService()

    @router.post("/signup")
    async def signup(body: SignUpDTO) -> JSONResponse:
        result = service.create_user(body.name, body.email, body.password)
        return JSONResponse(status_code=result["code"], content=result)
    
    @router.post("/signin")
    async def signin(body: SignInDTO) -> JSONResponse:
        result = service.authenticate_user(body.email, body.password)
        return JSONResponse(status_code=result["code"], content=result)

    @router.post("/signout")
    async def signout(user: User = Depends(extract_token)) -> JSONResponse:
        result = service.revoke_token(user.user_id)
        return JSONResponse(status_code=200, content=result)
    
    return router
