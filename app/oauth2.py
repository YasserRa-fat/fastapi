import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt

from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from app import models, schemas, databases
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
def create_access_token(data: dict()):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(  minutes= 60)
    to_encode.update({"exp": expire}) 
    
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
  try:
     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
     id: str = payload.get("user_id")
 
     if id is None:
        raise credentials_exception
     token_data = schemas.Tokendata(id=id)
  except JWTError as e:
     raise credentials_exception

  return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme),db:Session = Depends(databases.get_db)):
    credentials_exception = HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail=
                    "could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    token =  verify_access_token(token, credentials_exception)
    this_user = db.query(models.User).filter(models.User.id==token.id).first()
    return this_user