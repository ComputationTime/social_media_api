from .. import schemas, utils, models
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db

router = APIRouter(prefix="/users", tags=['Users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserPrivate)
def create_user(user: schemas.UserPost, db: Session = Depends(get_db)):
    queried = db.query(models.User).filter(
        models.User.username == user.username).first()
    if queried:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username already in use.")
    queried = db.query(models.User).filter(
        models.User.email == user.email).first()
    if queried:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already in use.")
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    return new_user


@router.get("/{id}", response_model=schemas.UserReturn)
def get_users(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {user_id} was not found.")
    return user
