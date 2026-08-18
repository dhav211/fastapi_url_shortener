from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.database import Base, engine, get_db
from src.models.url import Url
from src.routes.urls import router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/{short_code}")
async def redirect_to_short_code(short_code: str, db: Session = Depends(get_db)):
    url = db.query(Url).filter_by(short=short_code).first()
    if url:
        return RedirectResponse(url=f"https://{url.full}", status_code=302)
    else:
        raise HTTPException(status_code=404, detail=f"Short code {short_code} doesn't exist")

