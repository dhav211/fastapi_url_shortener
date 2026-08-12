from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.url import Url
from src.shorten import create_short_code

router = APIRouter(prefix="/api/v1/urls")

@router.post("/{url_shorten:path}")
async def shorten_url(url_shorten: str, db: Session = Depends(get_db)):
    short_code = create_short_code()
    db_url = Url(full=url_shorten, short=short_code, creation_date=date.today(), expiration_date=date.today())

    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url