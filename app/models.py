import sys
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from app.databases import  Base
from sqlalchemy.orm import relationship
from email.policy import default
from tokenize import String
from xmlrpc.client import Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, Table, ForeignKeyConstraint
from sqlalchemy.sql.expression import null

class Post(Base):
    __tablename__ =  "posts"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default= 'TRUE', nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), server_default = text('NOW()'),nullable = False )
    
   
    owner_id = Column(Integer, ForeignKey( 
            "users.id", ondelete="CASCADE"), nullable = False )
    #posts = relationship ("users", back_populates="id")
   # owner =  relationship("app.models.User", viewonly = True)
   # owner = relationship("app.models.User")
    
     #owner_id = relationship("app.models.User", back_populates="id")
    ForeignKeyConstraint
    
    
class User(Base):
      __tablename__ = 'users'
      __table_args__ = {'extend_existing': True}

      id = Column(Integer, primary_key=True, nullable=False)
      email = Column(String, nullable=False, unique=True )
      password = Column(String, nullable=False, )
      created_at = Column(TIMESTAMP(timezone=True), server_default = text('NOW()'),nullable = False )
      #owner = relationship("app.models.User")
      #parent = relationship("app.models.User", back_populates="owner")
      #child = relationship("app.models.Post", back_populates= "owner")
      
      
class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = {'extend_existing': True}

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE" ),primary_key=True)
    
    
    
    
          