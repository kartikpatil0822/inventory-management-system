import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


class Settings:
    """
    Settings class to manage and load environment variables for database and Redis configuration.

    :Attributes:
        POSTGRES_USER (str): PostgreSQL username from environment variables.
        POSTGRES_PASSWORD (str): PostgreSQL password from environment variables.
        POSTGRES_SERVER (str): PostgreSQL server address from environment variables.
        POSTGRES_PORT (str): PostgreSQL port from environment variables.
        POSTGRES_DB (str): PostgreSQL database name from environment variables.
        DATABASE_URL (str): Full PostgreSQL database URL constructed from the above variables.
        REDIS_HOST (str): Redis server address from environment variables.
        REDIS_PORT (str): Redis port from environment variables.
        REDIS_URL (str): Full Redis URL constructed from the above variables.
    """

    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_SERVER = os.environ.get('POSTGRES_SERVER')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
    POSTGRES_DB = os.environ.get('POSTGRES_DB')

    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = os.environ.get('REDIS_PORT')

    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"


settings = Settings()
