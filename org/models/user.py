from pydantic import BaseModel, EmailStr


class UserRequestModel(BaseModel):
    login: str
    first_name: str
    last_name: str
    password: str
    email: EmailStr | None


class UserResponseModel(BaseModel):
    login: str
    first_name: str
    last_name: str
    email: EmailStr | None
