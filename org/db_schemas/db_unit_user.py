from sqlalchemy import Column, String, ForeignKey, DateTime, Table
from sqlalchemy.sql import func

from ..db.db_conn import Base

UnitUser = Table('unit_user', Base.metadata,
                 Column('unit_id', String(32), ForeignKey('units.unit_id'), primary_key=True),
                 Column('login', String(32), ForeignKey('users.login'), primary_key=True),
                 Column('cr_date', DateTime(timezone=True), server_default=func.now()),
                 Column('upd_date', DateTime(timezone=True), onupdate=func.now())
                 )

UnitUser.__tablename__ = "unit_user"

