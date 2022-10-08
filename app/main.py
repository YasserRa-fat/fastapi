import sys
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app.databases import   engine
from app import models, config
from passlib.context import CryptContext
from fastapi import  FastAPI
from app.routers import post, user, auth, vote
import models 
from fastapi.middleware.cors import CORSMiddleware







app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated= 'auto')

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



 
@app.get("/")
def root():
    return{"message":"hello world"}