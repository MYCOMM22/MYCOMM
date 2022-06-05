import re
from fastapi import Depends, FastAPI, Response, status, HTTPException, Depends, APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
import calendar
import datetime
from fastapi.templating import Jinja2Templates
from typing import Optional
from ..mqtt import server
from ..security import manager


templates = Jinja2Templates(directory="pages")
router = APIRouter(
    prefix="/smartclass",
    tags=['smartclass'])


@router.get('/data')
def get_smartclass(db: Session = Depends(get_db)):
    user = db.query(models.smartclass).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found")

    return "user"


@router.post("/control")
async def acreate(request: Request, classstatus: Optional[str] = Form(False), classroom=Form(...), db: Session = Depends(get_db)):
    # print(classroom)
    classupdate = db.query(models.smartclass).filter(
        models.smartclass.classroom == classroom).first()
    # print(classstatus)
    classupdate.Switchstatus = bool(classstatus)
    db.add(classupdate)
    db.commit()
    db.refresh(classupdate)
    server.publish(f"{classroom[-1]}{str(classstatus)[0]}")
    return RedirectResponse("/smartclass/control", status_code=status.HTTP_302_FOUND)


@router.get("/control")
async def acreate(request: Request,  db: Session = Depends(get_db), email=Depends(manager)):

    class1 = db.query(models.smartclass).order_by(
        models.smartclass.id).all()
    # return class1

    return templates.TemplateResponse(
        "smartclass.html", {"request": request, "class1": class1}, status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/delete")
async def device_delete(id=Form(...), db: Session = Depends(get_db), email=Depends(manager)):
    post_q = db.query(models.smartclass).filter(models.smartclass.id == id)
    post = post_q.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")
    post_q.delete(synchronize_session=False)
    db.commit()
    return RedirectResponse("/smartclass/control", status_code=status.HTTP_302_FOUND)


@router.post("/smartclass_create_FE", status_code=status.HTTP_201_CREATED)
async def acreate(classname=Form(...), deviceid=Form(...), db: Session = Depends(get_db), email=Depends(manager)):

    new_user = models.smartclass(
        classroom=classname, power_consumption=deviceid, Switchstatus=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return RedirectResponse("/smartclass/control", status_code=status.HTTP_302_FOUND)


@router.post("/smartclass_create", status_code=status.HTTP_201_CREATED)
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
