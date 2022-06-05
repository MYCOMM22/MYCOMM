import schedule
from logging import exception
from sqlite3 import Cursor
from typing import Optional
from fastapi import Depends, FastAPI, Response, status, HTTPException, Request
from fastapi.params import Body
from pydantic import BaseModel, BaseSettings
from random import randrange

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.middleware.cors import CORSMiddleware

from typing import Optional, List

import time
from sqlalchemy.orm import Session


from . import models
from . import schemas, utils
from .database import engine, get_db
from . routers import admin, auth, device, user, smartclass, smartpole, dashboard
from .config import settings
from fastapi_login import LoginManager
from .security import manager

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(device.router)
app.include_router(smartpole.router)
app.include_router(smartclass.router)
app.include_router(dashboard.router)


# app.include_router(vote.router)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")


templates = Jinja2Templates(directory="pages")


class NotAuthenticatedException(Exception):
    pass


def not_authenticated_exception_handler(request, exception):

    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)


manager.not_authenticated_exception = NotAuthenticatedException
app.add_exception_handler(NotAuthenticatedException,
                          not_authenticated_exception_handler)


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, email=Depends(manager)):
    return RedirectResponse("/device/", status_code=status.HTTP_302_FOUND)


@app.post("/test")
async def read_item(data: schemas.smartpole):
    print(data)
    return data


@app.get("/smartpole", response_class=HTMLResponse)
async def read_item(request: Request, email=Depends(manager)):
    return RedirectResponse("/smartpole/", status_code=status.HTTP_302_FOUND)


@app.get("/smartclass", response_class=HTMLResponse)
async def read_item(request: Request, email=Depends(manager)):
    return RedirectResponse("/smartclass/control", status_code=status.HTTP_302_FOUND)
