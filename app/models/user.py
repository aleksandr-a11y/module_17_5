from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.routers.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import  slugify
#from app.models.task import Task
from app.backend.db import Base

class User(Base):
    __tablename__= 'users'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)
    tasks = relationship('Task', back_populates="user")

#from sqlalchemy.schema import CreateTable
#print(CreateTable(User.__table__))
