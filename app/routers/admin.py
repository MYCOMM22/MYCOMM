import re
from fastapi import Depends, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
import calendar
import datetime

router = APIRouter(
    prefix="/admin",
    tags=['Admin'])


@router.post("/admin_create", status_code=status.HTTP_201_CREATED, response_model=schemas.createreturn)
async def acreate(user: schemas.admin_create, db: Session = Depends(get_db)):
    # hast the password - user.password

    hasdhed_password = utils.hash(user.password)
    user.password = hasdhed_password

    new_user = models.admin(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/user_create", status_code=status.HTTP_201_CREATED, response_model=schemas.createreturn)
async def sacreate(user: schemas.user_create, otp: int, db: Session = Depends(get_db)):

    if otp != 9919:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect Otp")

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.user(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/get_admins')
def get_subadmins(db: Session = Depends(get_db)):
    user = db.query(models.admin).all()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"subadmin not found")

    return user


@router.get('/get_admin{phone}', response_model=schemas.createreturn)
def get_subadmins(phone: int, db: Session = Depends(get_db)):
    user = db.query(models.admin).filter(
        models.admin.phone == phone).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"admin with phone: {phone} not found")

    return user


@router.delete("/admin_delete", status_code=status.HTTP_204_NO_CONTENT)
async def sadelete(phone: int, db: Session = Depends(get_db)):
    post_q = db.query(models.admin).filter(models.admin.phone == phone)
    post = post_q.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")
    post_q.delete(synchronize_session=False)
    db.commit()
    return "successfully deleted"


@router.get('/get_users')
def get_user(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_admin)):
    user = db.query(models.user).all()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No users found")

    return user


@router.get('/get_user{phone}', response_model=schemas.get_user)
def get_user(phone: int, db: Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.phone == phone).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {phone} not found")

    return user


@router.delete("/user_delete", status_code=status.HTTP_204_NO_CONTENT)
async def udelete(phone: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_admin)):
    post_q = db.query(models.user).filter(models.user.phone == phone)
    post = post_q.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")
    post_q.delete(synchronize_session=False)
    db.commit()
    return "successfully deleted"
