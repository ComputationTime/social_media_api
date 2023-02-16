from .. import schemas, models, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import Optional
from ..database import get_db
router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get('/', response_model=list[(schemas.PostFullReturn)])
def get_posts(db: Session = Depends(get_db), limit: int = 10, offset: int = 0, query: Optional[str] = ""):
    posts_with_votes = db.query(models.Post, func.count(1).filter(models.Vote.dir > 0).label("likes"), func.count(1).filter(models.Vote.dir < 0).label("dislikes")).join(
        models.Vote, models.Vote.post_id == models.Post.post_id, isouter=True).filter(models.Post.published == True, models.Post.title.contains(query)).group_by(models.Post.post_id).offset(offset).limit(limit).all()
    return posts_with_votes


@router.get('/{post_id}', response_model=schemas.PostFullReturn)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.post_id ==
                                        post_id).filter(models.Post.published == True).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {post_id} was not found.")
    post_with_votes = db.query(models.Post, func.count(1).filter(models.Vote.dir > 0).label("likes"), func.count(1).filter(models.Vote.dir < 0).label("dislikes")).join(
        models.Vote, models.Vote.post_id == models.Post.post_id, isouter=True).filter(models.Post.published == True, models.Post.post_id == post_id).group_by(models.Post.post_id).first()

    return post_with_votes


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostReturn)
def create_post(post: schemas.PostPost, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id=user.user_id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def get_post(post_id: int, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.post_id == post_id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {post_id} was not found so could not be deleted.")
    if post.first().user_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Cannot delete posts by other users.")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=schemas.PostReturn)
def update_post(post_id: int, post: schemas.PostPut, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(
        models.Post.user_id == user.user_id)
    old_post = post_query.first()
    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {post_id} was not found so could not be updated.")
    if old_post.user_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
