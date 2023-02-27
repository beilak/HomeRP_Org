from sqlalchemy.sql import exists
from sqlalchemy import select

#from ..db.db_conn import DBConn
from ..db_schemas.db_user import User
from ..db.db_conn import ORGDatabase
#from ..db_schemas.db_unit import Unit
from .error import UserExist, UserAssignedUnit, UserNotFoundError
from ..models.user import UserRequestModel


class UserRepository:
    """User Repository"""

    def __init__(self, db_session) -> None:
        """Init."""
        self._db_session = db_session

    async def add(self, user: User) -> User:
        """Add user to DB"""
        async with self._db_session() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user

    async def get_by_login(self, login: str) -> User:
        """Read user from DB by login"""
        async with self._db_session() as session:
            users = await session.execute(select(User).filter(User.login == login))
            user = users.fetchone()
            if not user:
                raise UserNotFoundError(login)
            else:
                return user[0]

    async def get_by_login_list(self, login: list | None = None, offset=0, limit=100):
        """Read user's from DB by login's"""
        async with self._db_session() as session:
            statement = select(User).offset(offset).limit(limit)
            if login is not None:
                statement.filter(User.login.in_(login))
                result = await session.execute(statement)
            else:
                result = await session.execute(statement)
            return result.all()

    async def is_user_exist(self, login) -> bool:
        """Checking is login exist in DB"""
        try:
            user = await self.get_by_login(login)
            if user:
                return True
        except UserNotFoundError:
            return False
        return False
        #return exists(user).scalar()
        # async with self._db_session() as session:
            # #result = await session.execute(User).f exists().where(User.login == login))
            # #return await session.execute(select(User).where(User.login == login).scalar())
            # return await session.execute(select(User).where(User.login == login).scalar())
            # #return result.scalar()

    async def delete_user(self, login):
        """Delete user in DB"""
        async with self._db_session() as session:
            await session.execute(User).filter(User.login == login).delete()
            await session.commit()

    # async def join_to_unit(self, user: User, unit):
    #     with self._db_session() as session:
    #         if self.is_user_in_unit(user, unit.unit_id) is True:
    #             raise UserAssignedUnit(user, unit.unit_id)
    #         user.units.append(unit)
    #         await session.commit()


class UserService:
    """User Service"""

    def __init__(self, repository: UserRepository) -> None:
        """Init."""
        self._repository = repository

    async def create(self, cr_user: UserRequestModel) -> User:
        """Create user"""
        login = cr_user.login
        if await self._repository.is_user_exist(login) is True:
            raise UserExist(login)
        return await self._repository.add(User(**cr_user.dict()))

    async def get_users(self, login: list | None = None, offset=0, limit=100):
        """Read user's detail"""
        result = await self._repository.get_by_login_list(login=login, offset=offset, limit=limit)
        users = []
        for user in result:
            users.append(user[0])
        return users


    async def get_user(self, login):
        """Read user detail"""
        return await self._repository.get_by_login(login=login)

    async def delete_user(self, login):
        """Delete user"""
        await self._repository.delete_user(login)

    @staticmethod
    async def is_user_in_unit(user: User, unit_id):
        """Check is user joined in unit"""
        for exist_unit in user.units:
            if unit_id == exist_unit.unit_id:
                return True
        return False

    # async def join_to_unit(self, login: str, unit_id) -> User:
    #     user = self.get_user(login)
    #     self._repository.join_to_unit(user, unit)
    #
    #     user = session.query(User).filter(User.login == login).one()
    #         if self.is_user_in_unit(user, unit.unit_id) is True:
    #             raise UserAssignedUnit(user, unit.unit_id)
    #         user.units.append(unit)
    #         session.commit()
    #
    #     user = self.get_user(login)
    #     return await user
