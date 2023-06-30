from dependency_injector import containers
from dependency_injector.providers import Configuration, Singleton, Factory, Resource
from pydantic.env_settings import BaseSettings
from org.controllers import UserRepository, UserService, UnitService, UnitRepository
from org.db.db_conn import DBEngineProvider, ORGDatabase
from org.controllers.mq_event_cnt import MqEventCnt


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

    _user_repository: Factory[UserRepository] = Factory(
        UserRepository,
        db_session=_org_db.provided.new_session,
    )

    user_service: Factory[UserService] = Factory(
        UserService,
        repository=_user_repository,
    )

    _unit_repository: Factory[UnitRepository] = Factory(
        UnitRepository,
        db_session=_org_db.provided.new_session,
    )

    _mq_event_cnt: Resource[MqEventCnt] = Resource(
        MqEventCnt,
        mq_host=config.mq_host,
        mq_user=config.mq_user,
        mq_pwd=config.mq_pass,
        header_tech_info={"service": "org"},
        routing_key=config.mq_routing_key,
    )

    unit_service: Factory[UnitService] = Factory(
        UnitService,
        repository=_unit_repository,
        event_cnt=_mq_event_cnt,
    )

    @staticmethod
    def create_container(settings: BaseSettings) -> 'OrgContainer':
        """ Org container crater"""
        container: OrgContainer = OrgContainer()
        container.config.from_pydantic(settings)
        return container
