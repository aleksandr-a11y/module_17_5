from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.routers.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import  slugify
from app.models.user import User

from app.backend.db import Base

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    slug = Column(String, unique=True, index=True)

    user = relationship('User', back_populates="tasks")


