from app.config.envirenment import get_settings
from app.core.main import init_app

_S = get_settings()

app = init_app(_S)