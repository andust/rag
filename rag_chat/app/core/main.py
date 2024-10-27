from fastapi.applications import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from toolz import pipe

from app.api.routes import register_routers
from app.config.envirenment import Settings


def create_instance(settings: Settings) -> FastAPI:
    return FastAPI(debug=settings.IS_PRODUCTION is False)


def init_database(app: FastAPI) -> FastAPI:
    return app


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


def init_app(settings: Settings) -> FastAPI:
    app: FastAPI = pipe(
        settings,
        create_instance,
        init_database,
        register_middlewares,
        register_routers,
    )

    return app
