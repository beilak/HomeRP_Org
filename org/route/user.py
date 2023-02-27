""" User Route """

from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from dependency_injector.wiring import inject, Provide
from ..containers import OrgContainer
from ..models.user import UserResponseModel, UserRequestModel
#from ..models import UnitResponseModel, UserUnitResponseModel, UserUnitRequestModel
from ..controllers import UserService #, UnitFactory


user_router: APIRouter = APIRouter()


@user_router.get(
    "/users/",
    status_code=status.HTTP_200_OK,
    response_model=List[UserResponseModel],
)
@inject
async def get_users(
        skip: int = 0,
        limit: int = 100,
        user_service: UserService = Depends(Provide[OrgContainer.user_service]),
) -> List[UserResponseModel]:
    """Return list of users"""
    users = await user_service.get_users(offset=skip, limit=limit)
    users_out = []
    for user in users:
        users_out.append(UserResponseModel(**user.__dict__))
    return users_out


@user_router.get(
    "/users/{login}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseModel)
@inject
async def get_user(
        login: str,
        user_service: UserService = Depends(Provide[OrgContainer.user_service]),
) -> UserResponseModel:
    """Return user detail info"""
    user = await user_service.get_user(login)
    return UserResponseModel(**user.__dict__)


@user_router.post(
    "/users/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseModel)
@inject
async def create_user(
        user: UserRequestModel,
        user_service: UserService = Depends(Provide[OrgContainer.user_service]),
) -> UserResponseModel:
    """Posting new user"""
    created_user = await user_service.create(user)
    return UserResponseModel(**created_user.__dict__)


# @user_router.put(
#     "/users/{login}/join_to_unit",
#     status_code=status.HTTP_200_OK,
#     response_model=UserUnitResponseModel)
# @inject
# async def user_join_to_unit(
#         join: UserUnitRequestModel,
#         user_factory: UserService = Depends(Provide[OrgContainer.user_factory]),
#         unit_factory: UnitFactory = Depends(Provide[OrgContainer.unit_factory]),
# ):
#     """Join user to unit"""
#     unit = unit_factory.get_unit(join.unit_id)
#     user = user_factory.join_to_unit(join.login, unit)
#     units = [UnitResponseModel(**i.__dict__) for i in user.units]
#     return UserUnitResponseModel(login=user.login, units=units)
