""" User Route """

from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List
from dependency_injector.wiring import inject, Provide
from org.containers import OrgContainer
from org.models.user import UserResponseModel, UserRequestModel
from org.controllers import UserService
from org.controllers.error import UserExist


user_router: APIRouter = APIRouter()


@user_router.get(
    "/user",
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
    "/user/{login}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseModel
)
@inject
async def get_user(
        login: str,
        user_service: UserService = Depends(Provide[OrgContainer.user_service]),
) -> UserResponseModel:
    """Return user detail info"""
    user = await user_service.get_user(login)
    return UserResponseModel(**user.__dict__)


@user_router.post(
    "/user",
    description="register new user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseModel
)
@inject
async def create_user(
        response: Response,
        user: UserRequestModel,
        user_service: UserService = Depends(Provide[OrgContainer.user_service]),
) -> UserResponseModel:
    """Posting new user"""
    try:
        user = await user_service.create(user)
    except UserExist:
        response.status_code = 200
        user = await user_service.get_user(user.login)

    return UserResponseModel(**user.__dict__)


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
