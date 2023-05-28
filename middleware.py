from firebase_admin import auth
from firebase_admin._auth_utils import InvalidIdTokenError
from firebase_admin._token_gen import ExpiredIdTokenError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def validation_body_exception_handler(app: FastAPI) -> callable:
    @app.middleware("http")
    async def authorization_jwt(request: Request, call_next: callable):
        access_token = request.headers.get("Authorization").split()
        if len(access_token) != 2:
            return JSONResponse(status_code=401, content={"code": 401, "msg": "Invalid credentials"})

        if access_token[0] == "Bearer":
            return JSONResponse(status_code=401, content={"code": 401, "msg": "Invalid credentials"})

        id_token = access_token[1]

        try:
            user = auth.verify_id_token(id_token)
            request.headers.__dict__["_list"].append(("user", user))

        except ExpiredIdTokenError:
            return JSONResponse(status_code=401, content={"code": "Unauthorized"})

        except InvalidIdTokenError:
            return JSONResponse(status_code=401, content={"code": 401, "msg": "Invalid credentials"})

        except ValueError:
            return JSONResponse(status_code=401, content={"code": 401, "msg": "Invalid credentials"})

        except Exception as e:
            print(e)
            return JSONResponse(status_code=500, content={"code": 500, "msg": "Internal error"})

        response = await call_next(request)
        return response

    return authorization_jwt
