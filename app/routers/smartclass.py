import re
from fastapi import Depends, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
import calendar
import datetime

router = APIRouter(
    prefix="/smartclass",
    tags=['smartclass'])


@router.post("/smartclass_create", status_code=status.HTTP_201_CREATED, response_model=schemas.smartclass)
async def acreate(user: schemas.smartclass, db: Session = Depends(get_db)):
    # hast the password - user.password

    #hasdhed_password = utils.hash(user.password)
    #user.password = hasdhed_password

    new_user = models.smartclass(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/get_smartclass')
def get_smartclass(db: Session = Depends(get_db)):
    user = db.query(models.smartclass).all()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found")

    return user


@router.get('/get_smartclass{phone}', response_model=schemas.smartclass)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.smartclass).filter(
        models.smartclass.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"smartclass with id: {id} not found")

    return user


@router.delete("/smartclass_delete", status_code=status.HTTP_204_NO_CONTENT)
async def smart_classdelete(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_admin)):
    post_q = db.query(models.user).filter(models.smartclass.id == id)
    post = post_q.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")
    post_q.delete(synchronize_session=False)
    db.commit()
    return "successfully deleted"


@router.put("/smartclass{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_smartclass(id: int, user: schemas.smartclass, db: Session = Depends(get_db)):
    bay_q = db.query(models.smartclass).filter(models.smartclass.id == id)
    bay = bay_q.first()

    if id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")

    bay_q.update(user.dict(), synchronize_session=False)
    db.commit()
    return bay_q
