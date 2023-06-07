from typing import Optional

from pydantic import BaseModel, Field


class SignUpDTO(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=5, max_length=100)
    password: str = Field(min_length=8, max_length=100)

    class Config:
        schema_extra = {
            "example": {
                "name": "Aku butuh ini",
                "email": "akubutuhini@gmail.com",
                "password": "akubutuhini",
            }
        }


class SignInDTO(BaseModel):
    email: str = Field(max_length=100)
    password: str = Field(min_length=8, max_length=100)

    class Config:
        schema_extra = {
            "example": {"email": "akubutuhini@gmail.com", "password": "akubutuhini"}
        }


class RefreshTokenDTO(BaseModel):
    refresh_token: str = Field(min_length=1)

    class Config:
        schema_extra = {
            "example": {
                "refresh_token": "ceritanya-refresh-token-buat-pier-si-paling-solo-md",
            }
        }


class GetUserInfoBody(BaseModel):
    id_token: str = Field(min_length=1)

    class Config:
        schema_extra = {
            "example": {
                "id_token": "ceritanya-token-buat-pier-si-paling-solo-md",
            }
        }


class BaseResponse(BaseModel):
    code: int
    msg: str
    data: Optional[dict]


signup_response = {200: {"code": 201, "msg": "Created"}}
