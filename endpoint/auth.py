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

            Response: 201
            ```
            {
                "code": 201,
                "msg": "Created"
            }
            ```
        """
        result = service.create_user(body.name, body.email, body.password)
        return JSONResponse(status_code=result["code"], content=result)

    @router.post("/signin", status_code=200)
    async def signin(body: SignInDTO) -> JSONResponse:
        """
            Sign In / Login a user

            Response: 200
            ```
            {
                "code": 200,
                "msg": "OK",
                "data": {
                    "id": "lrGpw03KXZTy7ZW9Um2OO1Bxxr72",
                    "email": "useramboy@gmail.com",
                    "name": "Stop Futanari",
                    "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU0NWUyNDZjNTEwNmExMGQ2MzFiMTA0M2E3MWJiNTllNWJhMGM5NGQiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiU3RvcCBGdXRhbmFyaSIsInBpY3R1cmUiOiJodHRwczovL3N0YXRpYy52ZWN0ZWV6eS5jb20vc3lzdGVtL3Jlc291cmNlcy90aHVtYm5haWxzLzAwNC81MTEvMjgxL3NtYWxsL2RlZmF1bHQtYXZhdGFyLXBob3RvLXBsYWNlaG9sZGVyLXByb2ZpbGUtcGljdHVyZS12ZWN0b3IuanBnIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2N1a2ktNTU3M2YiLCJhdWQiOiJjdWtpLTU1NzNmIiwiYXV0aF90aW1lIjoxNjg2MTM5NTI5LCJ1c2VyX2lkIjoibHJHcHcwM0tYWlR5N1pXOVVtMk9PMUJ4eHI3MiIsInN1YiI6ImxyR3B3MDNLWFpUeTdaVzlVbTJPTzFCeHhyNzIiLCJpYXQiOjE2ODYxMzk1MjksImV4cCI6MTY4NjE0MzEyOSwiZW1haWwiOiJ1c2VyYW1ib3lAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsidXNlcmFtYm95QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.kId99QGlmjxDy7aYoRhvmm00o3F2WIuBy6o-KfZe8d8Q1pBNa4DehWPfcdGe6gHEgJFGr_c2-kY9TWyctEcpoihfH5C5Wpy3RE7KMO8SI-xKYqn8K_w2Bt2cdDyZ8JYFhJpYvSO5tcUlECFnkqFkDhF7yrtClthpaFOUOzvCY4qu6nybKX2Lqzyx_d-tV-CZi3c9tyo-berr4g3j0pTDtOuvkmDcR1gNt7v9xUESK_XUqtxErJ9mEx0ZMvEjqIQSOk9zh8uHm6nzh55GH8b9-6J7yvwxr3dG1ZUYw4q4ZSCAbiKyARsOazzhNYiIPasKFOEenJLvuRy5c0GOeTt-hA",
                    "refresh_token": "APZUo0TzBPHk8ya5V6ln1NAMw2hiIqnDKte9LDxDKM4HePtgosuT9kFG0C5PAKd3u9FA0ff_MrSp7yqmqm5B_4brUmPgxkzn3bO_j5az4WlYKaK4k1wWeG8B_DAq2mfTOAqZXepkK1y3wOKwYAqrnYCrVuYnEjW1HSMh6VRHPvcHwDbJGHNWpDOHhVjj6FCG8vinkEveO1g3RJF2bSDhqYZkwpfHIILY1A",
                    "expires_in": "3600"
                }
            }
            ```
        """
        result = service.authenticate_user(body.email, body.password)
        return JSONResponse(status_code=result["code"], content=result)

    @router.post("/signout", status_code=200)
    async def signout(user: User = Depends(extract_token)) -> JSONResponse:
        """
            Sign out / Logout a user \n
            **NOTE:** Requires a Bearer Token

            Response: 200
            ```
            {
                "code": 200,
                "msg": "OK"
            }
            ```
        """
        result = service.revoke_token(user.user_id)
        return JSONResponse(status_code=result["code"], content=result)

    @router.put("/refresh", status_code=200)
    async def refresh(body: RefreshTokenDTO) -> JSONResponse:
        """
            If your token has been expired, 
            use your refresh token to get a new token and new refresh token.

            Response: 200
            ```
            {
                "code": 200,
                "msg": "OK",
                "data": {
                    "id": "lrGpw03KXZTy7ZW9Um2OO1Bxxr72",
                    "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU0NWUyNDZjNTEwNmExMGQ2MzFiMTA0M2E3MWJiNTllNWJhMGM5NGQiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiU3RvcCBGdXRhbmFyaSIsInBpY3R1cmUiOiJodHRwczovL3N0YXRpYy52ZWN0ZWV6eS5jb20vc3lzdGVtL3Jlc291cmNlcy90aHVtYm5haWxzLzAwNC81MTEvMjgxL3NtYWxsL2RlZmF1bHQtYXZhdGFyLXBob3RvLXBsYWNlaG9sZGVyLXByb2ZpbGUtcGljdHVyZS12ZWN0b3IuanBnIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2N1a2ktNTU3M2YiLCJhdWQiOiJjdWtpLTU1NzNmIiwiYXV0aF90aW1lIjoxNjg2MTQwMDI0LCJ1c2VyX2lkIjoibHJHcHcwM0tYWlR5N1pXOVVtMk9PMUJ4eHI3MiIsInN1YiI6ImxyR3B3MDNLWFpUeTdaVzlVbTJPTzFCeHhyNzIiLCJpYXQiOjE2ODYxNDAwMzUsImV4cCI6MTY4NjE0MzYzNSwiZW1haWwiOiJ1c2VyYW1ib3lAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsidXNlcmFtYm95QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.GHumiyMHOsE3AgwfcGYtRLzJP0m5n1Lpy7dkt2rbnMGuv9pIG3W2dwQmiEug-mW-Pswl5hLDhM9bIEp22mhF9WmtAbNDf6a-eFRCHzr0A770qIn4c81NmCb96aEBO3sS_2ymOyli5vKB9GIlswgA-Ga0uG4JC_G_iTMSXfiQDM2Ef9us8Go6gazZXBErhAPUZIvJrN6RxDIw5tyNYSstClPz1FrOSTzn17CIijJxdsWl7DWgA2gFjF21EfP4kE2WgDaikp1-sUy8oywtD6nTQzsx2_lm9jClunPkLRG8HSgeCjAswn2x-7-kUlpd6TIWiQN0_451RQBLQhgaN96abg",
                    "refresh_token": "APZUo0SRj1QpmSn459aRsyYbS--tsbXULY_m2MwzSxibx39JzrVgUs7Z2MfrvmPLP_Vm_k-oEk2sUsmu81QA0ReV7rykH9EBXN77nndLr4nEog80rnzfBhxHZDJlXaM-aadN9olBEC3wI0E27ALj287Z9pRq8wi8qKWWbNHLuLxcD29PJgLIsgL4-aEQ2AH11m91P9YYa2zza_PNoNeoFZzknZOgqA6j3A",
                    "expires_in": "3600"
                }
            }
            ```
        """
        result = service.refresh_token(body.refresh_token)
        return JSONResponse(status_code=result["code"], content=result)

    @router.get('/me', status_code=200)
    async def me(user: User = Depends(extract_token)) -> JSONResponse:
        """
            Use your token to know who you are. \n
            **NOTE:** Requires a Bearer Token

            Response: 200
            ```
            {
                "code": 200,
                "msg": "OK",
                "data": {
                    "id": "lrGpw03KXZTy7ZW9Um2OO1Bxxr72",
                    "name": "Stop Futanari",
                    "email": "useramboy@gmail.com",
                    "photo_url": "https://static.vecteezy.com/system/resources/thumbnails/004/511/281/small/default-avatar-photo-placeholder-profile-picture-vector.jpg"
                }
            }
            ```
        """
        return JSONResponse(status_code=200, content={
            "code": 200,
            "msg": "OK",
            "data": {
                "id": user.user_id,
                "name": user.name,
                "email": user.email,
                "photo_url": user.photo_url
            }
        })

    return router
