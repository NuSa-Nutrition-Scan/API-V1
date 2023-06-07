from .dto import SignUpDTO, SignInDTO, RefreshTokenDTO, BaseResponse
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from service.authentication import AuthService
from .security import extract_token, User


def routes(service: AuthService) -> APIRouter:
    router = APIRouter(prefix='/auth', tags=["Authentication"])

    @router.post("/signup", status_code=201)
    async def signup(body: SignUpDTO) -> JSONResponse:
        """
            Sign Up / Create a new user
        """
        result = service.create_user(body.name, body.email, body.password)
        return JSONResponse(status_code=result["code"], content=result)

    @router.post("/signin", status_code=200)
    async def signin(body: SignInDTO) -> JSONResponse:
        """
            Sign In / Login a user
        """
        result = service.authenticate_user(body.email, body.password)
        return JSONResponse(status_code=result["code"], content=result)

    @router.post("/signout", status_code=200)
    async def signout(user: User = Depends(extract_token)) -> JSONResponse:
        """
            Sign out / Logout a user \n
            **NOTE:** Requires a Bearer Token
        """
        result = service.revoke_token(user.user_id)
        return JSONResponse(status_code=result["code"], content=result)

    @router.put("/refresh", status_code=200)
    async def refresh(body: RefreshTokenDTO) -> JSONResponse:
        """
            If your token has been expired, 
            use your refresh token to get a new token and new refresh token
        """
        result = service.refresh_token(body.refresh_token)
        return JSONResponse(status_code=result["code"], content=result)

    @router.get('/me', status_code=200)
    async def me(user: User = Depends(extract_token)) -> JSONResponse:
        """
            Use your token to know who you are. \n
            **NOTE:** Requires a Bearer Token
        """
        return JSONResponse(status_code=200, content=user)

    return router
