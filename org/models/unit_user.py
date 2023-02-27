from typing import List
from pydantic import BaseModel
from .user import UserResponseModel
from .unit import UnitResponseModel


class UserUnitRequestModel(BaseModel):
    login: str
    unit_id: str


class UserUnitResponseModel(BaseModel):
    login: str
    units: List[UnitResponseModel]


class UnitUserResponseModel(BaseModel):
    unit_id: str
    users: List[UserResponseModel]
