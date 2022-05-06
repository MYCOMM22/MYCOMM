from fastapi import Depends, FastAPI, Response, status, HTTPException, Depends, APIRouter, Request, Form
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2
from fastapi.responses import HTMLResponse, RedirectResponse
from ..database import get_db
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .auth import manager

# router.mount("/assets", StaticFiles(directory="assets"), name="assets")


templates = Jinja2Templates(directory="pages")


router = APIRouter(
    prefix="/user",
    tags=['User'])


@router.get("/create", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("sign-up.html", {"request": request})


@router.post('/create')
async def login(name=Form(...), email=Form(...), phone=Form(...), password=Form(...), db: Session = Depends(database.get_db)):
    # print(name)
    # print(username)
    # print(phone)
    # print(password)
    hasdhed_password = utils.hash(password)

    test_keys = ['name', 'email', 'phone', 'password']
    res = dict(zip(test_keys, [name, email, phone, hasdhed_password]))
    print(res)
    new_user = models.user(**res)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/profile")
def home(request: Request, email=Depends(manager), db: Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.email == email).first()
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})


@router.get('/profile')
def get_subadmins(db: Session = Depends(get_db)):
    user = db.query(models.admin).all()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"subadmin not found")

    return user
