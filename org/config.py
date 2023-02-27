from pydantic import BaseSettings


class Settings(BaseSettings):
    db_user = "org_test_user"
    db_pwd = "org_test_pwd"
    db_host = "127.0.0.1"
    db_port = "5431"
    db_name = "org_test"
