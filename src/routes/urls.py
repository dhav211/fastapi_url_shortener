from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.url import Url
from src.shorten import create_short_code, strip_url

router = APIRouter(prefix="/api/v1/urls")

@router.post("/{url_shorten:path}")
async def shorten_url(url_shorten: str, db: Session = Depends(get_db)):
    if db.query(Url).filter_by(full= strip_url(url_shorten)).first():
        raise HTTPException(
                    status_code=409,
                    detail=f"Url '{url_shorten}' already exists"
                )
    
    short_code = create_short_code()

    count = db.query(Url).count()

    while db.query(Url).filter_by(short= short_code).first() is not None:
        short_code = create_short_code()
    
    # check if short code is already in db
    db_url = Url(full=strip_url(url_shorten), short=short_code, creation_date=date.today(), expiration_date=date.today())

    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url