from fastapi import APIRouter, Depends
from org.containers import OrgContainer
from dependency_injector.wiring import Provide, inject
from org.controllers.tech.tech import TechService

checker_router: APIRouter = APIRouter()


@checker_router.get("/health", status_code=200)
async def health_check() -> None:
    """health check"""
    return None


@checker_router.get("/readiness", status_code=200)
@inject
async def readiness_check(
    tech_service: TechService = Depends(Provide[OrgContainer.tech_service])
) -> None:
    """readiness check"""
    await tech_service.check_db_connection()
    await tech_service.check_rabbit()
    return None
