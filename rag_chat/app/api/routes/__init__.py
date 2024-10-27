from fastapi.applications import FastAPI

from app.api.routes import root, chat
from app.config.envirenment import get_settings


_S = get_settings()
PREFIX = f"/api/{_S.API_VERSION}"


def register_routers(app: FastAPI) -> FastAPI:
    app.include_router(root.router, prefix=PREFIX)
    app.include_router(chat.router, prefix=PREFIX)

    return app
