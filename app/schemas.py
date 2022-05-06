
#from turtle import title
from selectors import BaseSelector
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime, date, time
from typing import Optional


class user_create(BaseModel):
    name: str
    username: str
    password: str


class user_get(BaseModel):
    name: str
    username: str
    phone: int


class user_profile(BaseModel):
    email: str
    name: str
    phone: str


class admin_create(BaseModel):
    email: str
    name: str
    phone: str
    password: str


class createreturn(BaseModel):
    id: int
    email: str
    name: str
    phone: str
    created_at: datetime

    class Config:
        orm_mode = True


# class user_create(admin_create):
#     pass


class get_user(createreturn):
    pass


class admin(BaseModel):
    email: str
    name: str
    phone: int
    password: str

    class Config:
        orm_mode = True


class user(BaseModel):
    email: str
    name: str
    phone: int
    password: str
    # created_at: datetime

    class Config:
        orm_mode = True


class smartclass(BaseModel):
    # id: int
    classroom: str
    power_consumption: float
    switch_status: bool

    class Config:
        orm_mode = True


class smartpole(BaseModel):

    # id = int
    polename: str
    Temperature: float
    Humidity: float
    Air_quality: float
    Co2_emission: float

    class Config:
        orm_mode = True


class device(BaseModel):
    # id = int
    chip_id: int
    mac_id: int
    user_id: int

    class Config:
        orm_mode = True


class Token (BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
