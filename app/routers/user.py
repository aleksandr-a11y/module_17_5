from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.routers.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import  slugify
from app.models import User, Task
from app.backend.db import Base

router = APIRouter(prefix='/user',tags=['user'])

@router.get('/')
async def aii_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

@router.get('/{user_id}')
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found")
    return user

@router.post('/create')
async def create_user(new_user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    db.execute(insert(User).values(username=new_user.username,
                                   firstname=new_user.firstname,
                                   lastname=new_user.lastname,
                                   age=new_user.age,
                                   slug=slugify(new_user.username)))
    db.commit()



    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}




@router.put('/update')
async def update_user(user_id: int, updated_user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    query = select(User).where(User.id == user_id)
    user = db.scalar(query)
    if user:
        db.execute(update(User).where(User.id == user_id).values(**updated_user.dict()))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")



@router.delete('/delete')
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(delete(Task).where(Task.user_id == user_id))
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User deleted successfully!'}
