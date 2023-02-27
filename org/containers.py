from dependency_injector import containers
from dependency_injector.providers import Configuration, Singleton, Factory
from pydantic.env_settings import BaseSettings
from org.controllers import UserRepository, UserService, UnitFactory
from org.db.db_conn import DBEngineProvider, ORGDatabase


class OrgContainer(containers.DeclarativeContainer):
    """Org. container"""

    wiring_config = containers.WiringConfiguration(modules=[".route.user", ".route.unit"])

    config: Configuration = Configuration()

    _db_engine: Singleton[DBEngineProvider] = Singleton(
        DBEngineProvider,
        db_user=config.db_user,
        db_pwd=config.db_pwd,
        db_host=config.db_host,
        db_port=config.db_port,
        db_name=config.db_name,
    )

    _org_db: Singleton[ORGDatabase] = Singleton(
        ORGDatabase,
        engine_provider=_db_engine,
    )

    user_repository: Factory[UserRepository] = Factory(
        UserRepository,
        db_session=_org_db.provided.new_session,
    )

    user_service: Factory[UserService] = Factory(
        UserService,
        repository=user_repository,
    )

    unit_factory: Singleton[UnitFactory] = Singleton(
        UnitFactory,
        db_session=_org_db.provided.session_factory,
    )

    @staticmethod
    def create_container(settings: BaseSettings) -> 'OrgContainer':
        """ Org container crater"""
        container: OrgContainer = OrgContainer()
        container.config.from_pydantic(settings)
        return container
