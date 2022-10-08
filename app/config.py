import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from dotenv import load_dotenv
load_dotenv() 
from pydantic import BaseSettings

import os
#print(os.environ.get(''))

class Settings(BaseSettings):
   database_hostname:str = os.environ.get('DATABASE_HOSTNAME')
   database_port: str = os.environ.get('DATABASE_PORT')
   database_password: str =  os.environ.get('DATABASE_PASSWORD')
   database_name: str = os.environ.get('DATABASE_NAME')
   database_username: str = os.environ.get('DATABASE_USERNAME')
   secret_key: str = os.environ.get('SECRET_KEY')
   algorithm: str = os.environ.get('ALGORITHM')
   access_token_expire_minutes: int = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')

settings = Settings()    
