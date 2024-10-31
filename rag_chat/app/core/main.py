from fastapi.applications import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from toolz import pipe

from app.api.routes import register_routers
from app.config.envirenment import get_settings

_S = get_settings()


def create_instance() -> FastAPI:
    return FastAPI(debug=_S.IS_PRODUCTION is False)


def register_middlewares(app: FastAPI) -> FastAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:7007",
            "http://localhost:3001",
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
