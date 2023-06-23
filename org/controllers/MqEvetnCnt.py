from org.db_schemas.db_unit import Unit
import aio_pika
from json import dumps


class MqEventCnt:
    """Event controller."""
    NEW_UNIT_POSTED_EVN = "NEW_UNIT_POSTED_EVN"

    def __init__(self, mq_dsn: str, mq_routing_key: str, header_tech_info: dict):
        self._connection = await aio_pika.connect_robust(mq_dsn)
        self._routing_key = mq_routing_key
        self._headers = header_tech_info

    def _send_event(self, event_name: str, body: dict[any, any]) -> None:
        """Sending event to MQ"""
        async with self._connection:
            channel = await self._connection.channel()

            await channel.default_exchange.publish(
                aio_pika.Message(
                    headers={
                        **self._headers,
                        "event_name": event_name,
                        },
                    body=dumps(body).encode(),
                ),
                routing_key=self._routing_key,
            )

    def new_unit_posted(self, new_unit: Unit) -> None:
        """Event - New Unit posted"""
        self._send_event(
            event_name=self.NEW_UNIT_POSTED_EVN,
            body=dict(new_unit),
        )
