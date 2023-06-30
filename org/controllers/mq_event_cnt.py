from org.db_schemas.db_unit import Unit
import aio_pika
from json import dumps


class MqEventCnt:
    """Event controller."""
    NEW_UNIT_POSTED_EVN = "NEW_UNIT_POSTED_EVN"

    def __init__(self, mq_host, mq_user: str, mq_pwd: str, header_tech_info: dict, routing_key: str):

        self._connection = None
        self._mq_dsn = f"amqp://{mq_user}:{mq_pwd}@{mq_host}/"
        self._headers = header_tech_info
        self._routing_key = routing_key

        self._org_event_exchange = None

    async def _send_event(self, event_name: str, body: dict[any, any]) -> None:
        """Sending event to MQ"""
        async with await aio_pika.connect_robust(self._mq_dsn) as conn:
            channel = await conn.channel()
            self._org_event_exchange = await channel.declare_exchange(
                'hrp', aio_pika.ExchangeType.DIRECT,
            )

            await self._org_event_exchange.publish(
                aio_pika.Message(
                    headers={
                        **self._headers,
                        "event_name": event_name,
                        },
                    body=dumps(body).encode(),
                ),
                routing_key=self._routing_key,
            )

    async def new_unit_posted(self, new_unit: Unit) -> None:
        """Event - New Unit posted"""
        await self._send_event(
            event_name=self.NEW_UNIT_POSTED_EVN,
            body={
                "unit_id" : new_unit.unit_id,
                "description" : new_unit.description,
                "new_unit" : new_unit.admin,
            }
        )
