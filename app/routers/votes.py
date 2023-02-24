from .. import schemas, models, oauth2
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db

router = APIRouter(prefix="/vote", tags=['Likes & Dislikes'])

# TODO handle vote.dir = {0, -1} cases


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(
        models.Post.post_id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    query = db.query(models.Vote).filter(models.Vote.post_id ==
                                         vote.post_id, models.Vote.user_id == user.user_id)
    result = query.first()
    if result:
        query.delete(synchronize_session=False)
        db.commit()
    if vote.dir != 0:
        new_vote = models.Vote(user_id=user.user_id,
                               post_id=vote.post_id, dir=vote.dir)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added new vote."}
    return {"message": "Vote has been deleted."}
