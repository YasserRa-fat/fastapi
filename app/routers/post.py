from unittest import result
from webbrowser import get
from app import oauth2
from .. import models, schemas
from fastapi import  Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. databases import  get_db
from typing import List, Optional
from sqlalchemy import func
router = APIRouter(
    prefix= "/posts", tags = ["Posts"]

)
#

@router.get("/" )
def get_posts(db: Session = Depends(get_db),
              current_user: str = Depends(oauth2.get_current_user), 
              
             limit: int = 10, skip:int=0, search: Optional[str] = "" , response_model=List[schemas.PostOut]):
 
  #ursor.execute("""SELECT * FROM posts""")
  #posts = cursor.fetchall()
    #print(limit)

        
   # posts= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, 
     isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return [results]


@router.post('/', status_code= status.HTTP_201_CREATED, response_model=list[schemas.Post])
def create_post(post:schemas.PostCreate, db: Session = Depends(get_db),
               current_user: int = Depends(oauth2.get_current_user)):
   # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #              (post.title, post.content, post.published))
    #new_post = cursor.fetchone
    #conn.commit()
    
    
    models.Post.owner_id = current_user.id
    print(current_user.email)    
    new_post = models.Post(owner_id= current_user.id ,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
   # return new_post
#,response_model= schemas.PostOut
@router.get("/{id}"  )
def get_post(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
   # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))   
    #this_post = cursor.fetchone()
    #post = find_post(id)
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, 
     isouter = True).group_by(models.Post.id).filter(models.Post.id==id).first()
    
    
    
    if not post: 
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                           detail= f"post with id {id} was not found")
   #     response.status_code = status.HTTP_404_NOT_FOUND
   #     return {'message':f"post with id {id} was not found"}
    return [post]   
   

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int,  db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)  ):
   
   # cursor.execute(""" DELETE  FROM posts WHERE id = %s RETURNING * """, (str(id),))     
    #deleted_post = cursor.fetchone()
    #onn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)            
    post = post_query.first()
   
    
    
    if post_query.first()== None:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"post with id {id} does not exist")
    
    if post.owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                              detail="not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)  

@router.put("/{id}", response_model= List[schemas.Post])
def update(id:int, post:schemas.PostCreate,  db: Session = Depends(get_db),
           current_user: int = Depends(oauth2.get_current_user)):
#     cursor.execute(""" UPDATE  posts SET title= %s, content= %s, published=%s WHERE id= %s RETURNING *  """,
#                    (post.title,post.content, post.published,str(id),))    
#     updated_post = cursor.fetchone()
#     conn.commit()
     post_query = db.query(models.Post).filter(models.Post.id==id)
     updated_post = post_query.first()
     
     if updated_post== None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"post with id {id} does not exist")
       
     if updated_post.owner_id != current_user.id :
           
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                          detail="not Authorized to perform requested action")
     post_query.update(post.dict(), synchronize_session=False)
     db.commit()
     return [post_query.first()]