from pydantic import BaseModel


class UnitRequestModel(BaseModel):
    unit_id: str
    description: str
    admin: str
    join_pass: str | None


class UnitResponseModel(BaseModel):
    unit_id: str
    description: str
    admin: str
