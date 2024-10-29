from typing import Callable

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    IS_PRODUCTION: bool
    API_VERSION: str
    OPENAI_API_KEY: str
    MONGO_CONNECTION: str
    MONGO_DB: str
    CLIENT_SERVICE: str


def _configure_initial_settings() -> Callable[[], Settings]:
    load_dotenv()
    settings = Settings()  # type: ignore

    def fn() -> Settings:
        return settings

    return fn


get_settings = _configure_initial_settings()
