from firebase_admin import auth
from firebase_admin._auth_utils import InvalidIdTokenError
from firebase_admin._token_gen import ExpiredIdTokenError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


class User:
    def __init__(self, id_user: str, name: str, email: str, photo_url: str, auth_token: str):
        self.user_id = id_user
        self.name = name
        self.email = email
        self.photo_url = photo_url
        self.auth_token = auth_token


def extract_token(token: HTTPAuthorizationCredentials = Depends(security)) -> User:
    if token.scheme != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    id_token = token.credentials

    try:
        credentials = auth.verify_id_token(id_token)
        user = User(id_user=credentials["user_id"],
                    name=credentials["name"], email=credentials["email"], photo_url=credentials["picture"], auth_token=id_token)
        return user

    except ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Unauthorized")

    except InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    except Exception as e:
        print('Extract Token:', e)
        raise HTTPException(status_code=500, detail="Internal error")
