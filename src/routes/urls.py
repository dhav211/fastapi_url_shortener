from datetime import datetime, timedelta

import pytz
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.url import Url
from src.shorten import create_short_code, strip_url
from src.valid_url import is_valid

router = APIRouter(prefix="/api/v1/urls")

@router.post("/")
async def shorten_url(url_shorten: str, db: Session = Depends(get_db)):
    if db.query(Url).filter_by(full= strip_url(url_shorten)).first():
        raise HTTPException(
                    status_code=409,
                    detail=f"Url '{url_shorten}' already exists"
                )

    if not await is_valid(url=url_shorten):
        raise HTTPException(
                    status_code=400,
                    detail=f"Url '{url_shorten}' cannot be reached"
                )
    
    short_code = create_short_code()

    # if short code was already taken then retry making until an unused one is created
    while db.query(Url).filter_by(short= short_code).first() is not None:
        short_code = create_short_code()
    
    db_url = Url(
        full=strip_url(url_shorten), 
        short=short_code, 
        creation_date= datetime.now(tz=pytz.utc).date(), 
        expiration_date=datetime.now(tz=pytz.utc).date() + timedelta(days=30)
    )

    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url