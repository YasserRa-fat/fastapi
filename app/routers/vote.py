from fastapi import  Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, databases, models, oauth2


router = APIRouter(
    prefix="/vote", 
    tags=['Vote']
    
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session= Depends(databases.get_db)
         , current_user:int= Depends(oauth2.get_current_user) ):
  vote_query = db.query(models.Vote).filter(models.Vote.
     post_id==vote.post_id, models.Vote.user_id == current_user.id )  
  found_vote  =vote_query.first()
  post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
  if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"post with id {vote.post_id} does not exist")
  
  if(vote.dir==1):
     if found_vote:
         raise HTTPException(status_code=status.HTTP_409_CONFLICT,
           detail=f"user {current_user.id} has already voted on post {vote.post_id} ")
     new_vote = models.Vote(post_id= vote.post_id, user_id = current_user.id )
     db.add(new_vote)
     db.commit()
     return{"message":"added vote"}
  else:    
      if not found_vote:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                              detail="vote does not exist")
          
      vote_query.delete(synchronize_session=False)
      db.commit()
      return{"message":"vote deleted"}    
  
  
  
  
  