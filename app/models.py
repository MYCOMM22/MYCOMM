from sqlite3 import Timestamp
import string
from typing import Text
from sqlalchemy import Boolean, Column, Date, Integer, String, Time, column, ForeignKey, BigInteger
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base


class admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    name = Column(String,  nullable=False)
    phone = Column(BigInteger, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


class user(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String,  nullable=False, unique=True)
    name = Column(String,  nullable=False)
    phone = Column(BigInteger, nullable=False)
    password = Column(String, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
