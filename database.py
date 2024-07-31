from typing import Generator

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

DB_URL = settings.DATABASE_URL

engine = create_engine(DB_URL, echo=True, pool_pre_ping=True)

Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator:
    try:
        db = Session()
        yield db
    finally:
        db.close()


async def get_redis_pool():
    redis_instance = redis.Redis.from_url(url=settings.REDIS_URL)
    return redis_instance
