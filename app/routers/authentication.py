from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, utils, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/login", tags=['Authentication'])


@router.post("/", response_model=schemas.Token)
def login(provided: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == provided.username).first()
    if not user or not utils.verify(user.password, provided.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Incorrect email or password.")
    access_token = oauth2.create_access_token(data={"user_id": user.user_id})

    return {"access_token": access_token, "token_type": "bearer"}
