from decouple import config, RepositoryEnv, Config
import os
from authx import AuthXConfig, AuthX

config_jwt = AuthXConfig()
config_jwt.JWT_SECRET_KEY = 'secret'
config_jwt.JWT_ACCESS_COOKIE_NAME = 'access_token'
config_jwt.JWT_TOKEN_LOCATION = ['cookies']
config_jwt.JWT_COOKIE_CSRF_PROTECT = False
config_jwt.JWT_COOKIE_SECURE = False
config_jwt.JWT_COOKIE_SAMESITE = 'lax'

security = AuthX(config_jwt)

env_path = os.path.join(os.path.dirname(__file__),'..',"config","dev.env")
config = Config(RepositoryEnv(env_path))





DATABASE_URL = f"postgresql+asyncpg://{config('DB_USERNAME')}:{config('DB_PASSWORD')}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}"
