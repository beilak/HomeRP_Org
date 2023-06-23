""" Unit Route """

from fastapi import APIRouter, Depends, status, HTTPException, Response
from org.models import UnitResponseModel, UnitRequestModel
from org.containers import OrgContainer
from org.controllers import UnitService
from typing import List
from dependency_injector.wiring import inject, Provide
from org.controllers.error import UnitExist

unit_router: APIRouter = APIRouter()


@unit_router.post(
    "/unit",
    status_code=status.HTTP_201_CREATED,
    response_model=UnitResponseModel,
)
@inject
async def create_unit(
        response: Response,
        unit: UnitRequestModel,
        unit_service: UnitService = Depends(Provide[OrgContainer.unit_service]),
):
    """Post unit"""
    try:
        unit = await unit_service.create(unit)
    except UnitExist:
        response.status_code = 200
        unit = await unit_service.get_unit(unit.unit_id)

    return UnitResponseModel(**unit.__dict__)


@unit_router.get(
    "/unit",
    status_code=status.HTTP_200_OK,
    response_model=List[UnitResponseModel],
)
@inject
async def get_units(
        skip: int = 0,
        limit: int = 100,
        unit_service: UnitService = Depends(Provide[OrgContainer.unit_service]),
):
    units = await unit_service.get_units(offset=skip, limit=limit)
    unit_out = []
    for unit in units:
        unit_out.append(UnitResponseModel(**unit.__dict__))
    return unit_out


@unit_router.get(
    "/unit/{unit_id}",
    response_model=UnitResponseModel,
)
@inject
async def get_unit(
        unit_id: str,
        unit_service: UnitService = Depends(Provide[OrgContainer.unit_service]),
):
    unit = await unit_service.get_unit(unit_id)
    return UnitResponseModel(**unit.__dict__)
