from pydantic import BaseSettings


class Settings(BaseSettings):
    db_user: str
    db_pwd: str
    db_host: str
    db_port: int
    db_name: str
