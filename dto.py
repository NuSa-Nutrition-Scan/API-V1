from pydantic import BaseModel

class AuthBody(BaseModel):
    email: str
    password: str

class RefreshTokenBody(BaseModel):
    refresh_token: str

class GetUserInfoBody(BaseModel):
    id_token: str