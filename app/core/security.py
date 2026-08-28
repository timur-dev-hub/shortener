from datetime import timedelta
from authx import AuthX, AuthXConfig

from app.core.config import settings

config = AuthXConfig()
config.JWT_SECRET_KEY = settings.JWT_SECRET_KEY
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)


config.JWT_COOKIE_CSRF_PROTECT = False

security = AuthX(config=config)

