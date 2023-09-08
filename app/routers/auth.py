from fastapi import FastAPI, HTTPException, Response, status, APIRouter
from fastapi.params import Body, Depends
# here pydantic is the library which is already in env because we have used fastapi[all]
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from ..database import engine, get_db
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
    )

@router.post("/login",response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    
    # Filter the id, password
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    
    # Check If user is exist or not
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid credentials")
    
    # check if the password is matched or not
    # utils.verify is coming from utils.py file
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid credentials")

    # Create a token
    # return token
    access_token = oauth2.create_access_token(data = {"user_id":user.id})

    return {"access_token":access_token,"token_type":"bearer"}