from fastapi import APIRouter, Depends, status, HTTPException #, Response
from sqlalchemy.orm.session import Session

from app import database as db, models, schemas, oauth2

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session=Depends(db.get_db), current_user: dict=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).get(ident=vote.post_id)
    if not post:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist")
            
    q = db.query(models.Vote).filter(models.Vote.user_id==current_user.id, models.Vote.post_id==vote.post_id)
    found_vote = q.first()
    if vote.dir == 1:
        if found_vote:
            return HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already voted on this post")
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist")
        q.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}