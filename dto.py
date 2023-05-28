from pydantic import BaseModel, Field


class AuthBody(BaseModel):
    name: str = Field(max_length=50)
    email: str = Field(max_length=100)
    password: str = Field(min_length=8, max_length=100)


class RefreshTokenBody(BaseModel):
    refresh_token: str


class GetUserInfoBody(BaseModel):
    id_token: str
