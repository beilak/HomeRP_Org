""" Unit Route """

from fastapi import APIRouter, Depends, status, HTTPException
from org.models import UnitResponseModel, UnitRequestModel
from org.containers import OrgContainer
from org.controllers import UnitFactory
from typing import List
from dependency_injector.wiring import inject, Provide

unit_router: APIRouter = APIRouter()


@unit_router.post(
    "/units/",
    status_code=status.HTTP_201_CREATED,
    response_model=UnitResponseModel,
)
@inject
async def create_unit(
        unit: UnitRequestModel,
        unit_factory: UnitFactory = Depends(Provide[OrgContainer.unit_factory]),
):
    """Post unit"""
    # ToDo Remove exception into func.
    if unit_factory.is_unit_exist(unit.unit_id) is True:
        raise HTTPException(status_code=409, detail="Unit already exist")
    try:
        created_unit = unit_factory.create(unit)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    return UnitResponseModel(**created_unit.__dict__)


@unit_router.get(
    "/units/",
    status_code=status.HTTP_200_OK,
    response_model=List[UnitResponseModel],
)
@inject
async def get_units(
        skip: int = 0,
        limit: int = 100,
        unit_factory: UnitFactory = Depends(Provide[OrgContainer.unit_factory]),
):
    units = unit_factory.get_units(offset=skip, limit=limit)
    unit_out = []
    for unit in units:
        unit_out.append(UnitResponseModel(**unit.__dict__))
    return unit_out


@unit_router.get(
    "/units/{unit_id}",
    response_model=UnitResponseModel,
)
@inject
async def get_unit(
        unit_id: str,
        unit_factory: UnitFactory = Depends(Provide[OrgContainer.unit_factory]),
):
    unit = unit_factory.get_unit(unit_id)
    return UnitResponseModel(**unit.__dict__)
