from fastapi import FastAPI

from database import get_db, engine
from schemas.models import Base
from router import items_route

app = FastAPI()
app.dbx = get_db()
Base.metadata.create_all(bind=engine)
app.include_router(items_route.router)
