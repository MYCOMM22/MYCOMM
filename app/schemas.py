
#from turtle import title
from selectors import BaseSelector
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime, date, time
from typing import Optional


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


class user_create(admin_create):
    pass


class get_user(createreturn):
    pass


class sadelete(BaseModel):
    phone: int


class bay(BaseModel):
    bay_name: str
    product_id: int


class createslot(BaseModel):
    truck: str
    bay_id: int
    product_id: int
    slot_date: date
    slot_time: time


class createslot_id(BaseModel):

    slot_id: int


class bay_update(BaseModel):
    product_id: int


class update_slot(BaseModel):
    slot_date: str
    slot_time: str


class returnbooked(BaseModel):
    bay: int
    slot_date: date
    slot_time: time
    status: bool

    class Config:
        orm_mode = True


class Token (BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class product(BaseModel):
    product: str


class client(BaseModel):
    client: str


class clients_products(BaseModel):
    client_id: int
    product_id: int


class slot_60(BaseModel):
    #id: int
    slot: time
    #booked: bool

    class Config:
        orm_mode = True


class slot_30(BaseModel):
    #id: int
    slot: time
    #booked: bool

    class Config:
        orm_mode = True


class days_10(BaseModel):

    #id = int
    bay_id: int
    date: date
    slot: time
    booked: bool

    class Config:
        orm_mode = True


class month(BaseModel):
    #id = int
    working: bool
    date: date
    no_of_bays_working60: int
    no_of_bays_working30: int

    class Config:
        orm_mode = True


class days_10(BaseModel):
    bay_id: int
    date: date
    slot: time
