from decouple import config, RepositoryEnv, Config
import os

DATABASE_URL = f"postgresql+asyncpg://{config('DB_USERNAME')}:{config("DB_PASSWORD")}5@{config('DB_HOST')}:{config('DB_PORT')}/{config("DB_NAME")}"
