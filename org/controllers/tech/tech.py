"""Service for Tech"""
import json
import logging
from org.db.db_conn import ORGDatabase
# from sqlalchemy.ext.asyncio import AsyncSession
from org.controllers.mq_event_cnt import MqEventCnt
from sqlalchemy.sql import text


class TechService:
    """Tech Service"""

    def __init__(
            self,
            db_session,
            mq_event_cnt: MqEventCnt
    ):
        self._db_session = db_session
        self._mq_event_cnt = mq_event_cnt


    async def check_db_connection(self) -> None:
        async with self._db_session() as session:
            await session.execute(text("SELECT 1;"))

    async def check_rabbit(self) -> None:
        await self._mq_event_cnt.check_conn()
