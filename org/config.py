from pydantic import BaseSettings


class Settings(BaseSettings):
    db_user: str
    db_pwd: str
    db_host: str
    db_port: int
    db_name: str
    mq_host: str
    mq_user: str
    mq_pass: str
    mq_routing_key: str
