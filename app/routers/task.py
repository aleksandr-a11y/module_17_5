from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.routers.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import  slugify
from app.models import User, Task
from app.backend.db import Base

router = APIRouter(prefix='/task',tags=['task'])

@router.get('/')
async def aii_tasks(db: Annotated[Session, Depends(get_db)]):
    task = db.scalars(select(Task)).all()
    return task


@router.get('/task_id')
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found")
    return task


@router.post('/create')
async def create_task(new_task: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found")

    task_new = Task(
        title=new_task.title,
        content=new_task.content,
        priority=new_task.priority,
        completed=False,
        user_id=user_id,
        slug=slugify(new_task.title)
    )
    db.add(task_new)
    db.commit()
    return{'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put('/update')
async def update_task(task_id: int, updated_task: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    query = select(Task).where(Task.id == task_id)
    task = db.scalar(query)
    if task:
        db.execute(update(Task).where(Task.id == task_id).values(**updated_task.dict()))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "Task update is successful!"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")

@router.delete('/delete')
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    query = select(Task).where(Task.id == task_id)
    task = db.scalar(query)
    if task:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "Task deletion successful!"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")
