from .containers import OrgContainer
from .config import Settings
from typing import Final
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from .route import user_router #, unit_router
from .exceptions import valid_except_handler, http_except_handler


ORG_APP: FastAPI


async def service_startup() -> None:
    """ Init service """
    settings: Settings = Settings()
    container: Final[OrgContainer] = OrgContainer.create_container(settings)
    container.init_resources()
    ORG_APP.__container = container


async def service_shutdown() -> None:
    ...


_API_VER = "v1"
_API_PREFIX = f"/api/{_API_VER}"
ORG_APP = FastAPI(
    title="Organization service",
    description="Organization service controller",
    version=_API_VER,
    docs_url=f"{_API_PREFIX}/doc",
    on_startup=[service_startup],
    on_shutdown=[service_shutdown],
    )

ORG_APP.include_router(user_router, prefix=_API_PREFIX, tags=["Users"])
#ORG_APP.include_router(unit_router, prefix=_API_PREFIX, tags=["Units"])

ORG_APP.add_exception_handler(RequestValidationError, valid_except_handler)
ORG_APP.add_exception_handler(StarletteHTTPException, http_except_handler)
