import os

from sqlalchemy.sql import exists

#from org.db.db_conn import DBConn
from org.db_schemas.db_unit import Unit
from org.models import UnitRequestModel
from org.controllers.error import UnitExist, UnitNotFoundError
from sqlalchemy import select
from org.controllers.mq_event_cnt import MqEventCnt


class UnitRepository:

    def __init__(self, db_session) -> None:
        """Init."""
        self._db_session = db_session

    async def add(self, unit: Unit):
        async with self._db_session() as session:
            session.add(unit)
            await session.commit()
            await session.refresh(unit)
        return unit

    async def is_unit_exist(self, unit_id):
        try:
            unit = await self.get_unit(unit_id)
            if unit:
                return True
        except UnitNotFoundError:
            return False
        return False

    async def get_unit(self, unit_id):
        # with DBConn.get_new_session() as session:
        #     return session.query(Unit).filter(Unit.unit_id == unit_id).one()
        #
        async with self._db_session() as session:
            units = await session.execute(select(Unit).filter(Unit.unit_id == unit_id))
            unit = units.fetchone()
            if not unit:
                raise UnitNotFoundError(unit_id)
            else:
                return unit[0]

    async def get_units(self, offset=0, limit=100):
        async with self._db_session() as session:
            statement = select(Unit).offset(offset).limit(limit)
            result = await session.execute(statement)
            return result.all()

    # @classmethod
    # async def delete_unit(cls, unit):
    #     with DBConn.get_new_session() as session:
    #         session.query(Unit).filter(Unit.unit_id == unit.unit_id).delete()
    #         session.commit()


class UnitService:
    """User Service"""

    def __init__(
            self,
            repository: UnitRepository,
            event_cnt: MqEventCnt,
    ) -> None:
        """Init."""
        self._repository = repository
        self._event_cnt = event_cnt

    async def create(self, cr_unit: UnitRequestModel) -> Unit:
        """Create user"""
        if await self._repository.is_unit_exist(cr_unit.unit_id):
            raise UnitExist(cr_unit.unit_id)
        new_unit = await self._repository.add(
            Unit(**cr_unit.dict()),
        )
        await self._event_cnt.new_unit_posted(new_unit)
        return new_unit

    async def get_units(self, offset=0, limit=100):
        """Read user's detail"""
        result = await self._repository.get_units(offset=offset, limit=limit)
        users = []
        for user in result:
            users.append(user[0])
        return users

    async def get_unit(self, unit_id):
        """Read unit detail"""
        return await self._repository.get_unit(unit_id=unit_id)

    # async def delete_user(self, login):
    #     """Delete user"""
    #     await self._repository.delete_user(login)
