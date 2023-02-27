from sqlalchemy import String, Column, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy_utils import PasswordType

from ..db.db_conn import Base
from .db_unit_user import UnitUser
from .db_user import User


class Unit(Base):
    __tablename__ = "units"
    unit_id_type = String(32)
    unit_id = Column(unit_id_type, primary_key=True)
    description = Column(String(32))
    admin = Column(String(32), ForeignKey("users.login"), nullable=False)
    join_pass = Column(PasswordType(schemes=['pbkdf2_sha512']))
    cr_date = Column(DateTime(timezone=True), server_default=func.now())
    upd_date = Column(DateTime(timezone=True), onupdate=func.now())
    users = relationship(User, secondary=UnitUser, uselist=True,
                         back_populates="units", lazy='joined')
