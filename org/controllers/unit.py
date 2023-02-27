import os

from sqlalchemy.sql import exists

#from ..db.db_conn import DBConn
from ..db_schemas.db_unit import Unit
from ..models import UnitRequestModel
from .error import UnitExist


class UnitFactory:

    @classmethod
    async def create(cls, unit_in: UnitRequestModel):
        unit_id = unit_in.unit_id
        if cls.is_unit_exist(unit_id) is True:
            raise UnitExist(unit_id)

        if unit_in.join_pass is None:
            unit_in.join_pass = os.urandom()
        unit = Unit(**unit_in.__dict__)
        DBConn.insert((unit,))
        unit = cls.get_unit(unit_id)
        return unit

    @classmethod
    async def is_unit_exist(cls, unit_id):
        with DBConn.get_new_session() as session:
            return session.query(exists().where(Unit.unit_id == unit_id)).scalar()

    @classmethod
    async def get_unit(cls, unit_id):
        with DBConn.get_new_session() as session:
            return session.query(Unit).filter(Unit.unit_id == unit_id).one()

    @classmethod
    async def get_units(cls, offset=0, limit=100):
        with DBConn.get_new_session() as session:
            query = session.query(Unit).offset(offset).limit(limit)
            return query.all()

    @classmethod
    async def delete_unit(cls, unit):
        with DBConn.get_new_session() as session:
            session.query(Unit).filter(Unit.unit_id == unit.unit_id).delete()
            session.commit()
