from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy_utils import PasswordType, EmailType

from ..db.db_conn import Base
from ..db_schemas.db_unit_user import UnitUser


class User(Base):
    __tablename__ = "user"
    user_login_type = String(32)
    login = Column(user_login_type, primary_key=True)
    password = Column(PasswordType(schemes=['pbkdf2_sha512']))
    first_name = Column(String(32))
    last_name = Column(String(32))
    email = Column(EmailType)
    cr_date = Column(DateTime(timezone=True), server_default=func.now())
    upd_date = Column(DateTime(timezone=True), onupdate=func.now())
    # units = relationship('Unit', secondary=UnitUser, uselist=True,
    #                      back_populates="users", lazy='joined')
