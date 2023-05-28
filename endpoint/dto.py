from pydantic import BaseModel, Field


class SignUpDTO(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=5, max_length=100)
    password: str = Field(min_length=8, max_length=100)


class SignInDTO(BaseModel):
    email: str = Field(max_length=100)
    password: str = Field(min_length=8, max_length=100)


class RefreshTokenDTO(BaseModel):
    refresh_token: str


class GetUserInfoBody(BaseModel):
    id_token: str
