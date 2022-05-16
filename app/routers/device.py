import re
from fastapi import Depends, FastAPI, Response, status, HTTPException, Depends, APIRouter, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from .. import models, schemas, utils, oauth2
from ..database import get_db
import calendar
import datetime

import string
import random  # define the random module
from .auth import manager

from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="pages")

router = APIRouter(
    prefix="/device",
    tags=['Device'])


# routes with html response

@router.get('/mang')
def get_devices(request: Request, db: Session = Depends(get_db)):
    user = list(db.query(models.device).all())

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"device not found")

    return templates.TemplateResponse("dashboard.html", {"request": request, "devices": user})


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def acreate(mac_id=Form(...), chip_id=Form(...),  db: Session = Depends(get_db)):
    S = 32  # number of characters in the string.
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))

    new_user = models.device(
        chip_id=chip_id, mac_id=mac_id, user_id=1, api_key=ran)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return RedirectResponse("/device/mang", status_code=status.HTTP_302_FOUND)


@router.post("/delete")
async def device_delete(id=Form(...), db: Session = Depends(get_db)):
    post_q = db.query(models.device).filter(models.device.id == id)
    post = post_q.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")
    post_q.delete(synchronize_session=False)
    db.commit()
    return RedirectResponse("/device/mang", status_code=status.HTTP_302_FOUND)


# routes without html response


@router.post("/create_device", status_code=status.HTTP_201_CREATED, response_model=schemas.device)
async def acreate(user: schemas.device,   db: Session = Depends(get_db)):
    #user = db.query(models.user).filter(models.user.email == email).first()

    S = 32  # number of characters in the string.
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))

    new_user = models.device(**user.dict(), user_id=1, api_key=ran)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/get_devices')
def get_devices(db: Session = Depends(get_db)):
    user = db.query(models.device).all()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"device not found")

    return user


@router.get('/get_device{id}', response_model=schemas.device)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.device).filter(
        models.device.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with phone: {id} not found")

    return user


@router.delete("/device_delete", status_code=status.HTTP_204_NO_CONTENT)
async def device_delete(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_admin)):
    post_q = db.query(models.user).filter(models.device.id == id)
    post = post_q.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")
    post_q.delete(synchronize_session=False)
    db.commit()
    return "successfully deleted"


@router.put("/device{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_admin(id: int, user: schemas.admin, db: Session = Depends(get_db)):
    bay_q = db.query(models.user).filter(models.device.id == id)
    bay = bay_q.first()

    if id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")

    bay_q.update(user.dict(), synchronize_session=False)
    db.commit()
