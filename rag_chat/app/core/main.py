from contextlib import asynccontextmanager

from fastapi.applications import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from toolz import pipe

import motor
from beanie import init_beanie

from app.api.routes import register_routers
from app.config.envirenment import get_settings
from app.models import __beanie_models__

_S = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = motor.motor_asyncio.AsyncIOMotorClient(_S.MONGO_CONNECTION)  # type: ignore
    await init_beanie(database=client[_S.MONGO_DB], document_models=__beanie_models__)
    yield
    client.close()


def create_instance() -> FastAPI:
    return FastAPI(debug=_S.IS_PRODUCTION is False, lifespan=lifespan)


def register_middlewares(app: FastAPI) -> FastAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:7007",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def init_app() -> FastAPI:
    app: FastAPI = pipe(
        create_instance(),
        register_middlewares,
        register_routers,
    )

    return app
