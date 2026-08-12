from fastapi import FastAPI

from src.database import Base, engine
from src.models.url import Url
from src.routes.urls import router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}