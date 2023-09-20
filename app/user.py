from datetime import datetime
from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from .database import get_db

router = APIRouter()


@router.get('/')
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return {'status': 'success', 'results': len(users), 'users': users}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(payload: schemas.UserBaseSchema, db: Session = Depends(get_db)):
    new_user = models.User(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": "success", "user": new_user}


@router.patch('/{userId}')
def update_user(userId: str, payload: schemas.UserBaseSchema, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == userId)
    db_user = user_query.first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with this id: {userId} found')
    update_data = payload.dict(exclude_unset=True)
    user_query.filter(models.User.id == userId).update(update_data,
                                                       synchronize_session=False)
    db.commit()
    db.refresh(db_user)
    return {"status": "success", "user": db_user}


@router.get('/{userId}')
def get_user(userId: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == userId).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user with this id: {id} found")
    return {"status": "success", "user": user}


@router.delete('/{userId}')
def delete_user(userId: str, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == userId)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with this id: {id} found')
    user_query.delete(synchronize_session=False)
    db.commit()
    return {"status": "success","message":"user deleted successfully" }
