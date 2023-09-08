from fastapi import FastAPI, HTTPException, Response, status, APIRouter
from fastapi.params import Body, Depends
# here pydantic is the library which is already in env because we have used fastapi[all]
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from ..database import engine, get_db
from .. import models, schemas
from sqlalchemy.orm import Session
from .. import utils

# Binding the models
models.Base.metadata.create_all(bind=engine)

# tags params is used to add tag for FastAPI doc, It's not required
router = APIRouter(
    tags=['Users']
)

@router.post("/create_users", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):
    
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_cursor = models.User(**user.dict())
    db.add(new_cursor)
    db.commit()
    db.refresh(new_cursor)

    return new_cursor

# Get the user's detail'

@router.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"User with id : {id} does not exist!")
    return user