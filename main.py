from fastapi import FastAPI

from database import get_db, engine
from schemas.models import Base
from router import items_route

# FastAPI object
app = FastAPI()

# Database
app.dbx = get_db()

# Create Table
Base.metadata.create_all(bind=engine)

# Include router
app.include_router(items_route.router)
