from sqlalchemy.orm import Session
import app.models as models, app.schemas as schemas
from fastapi import HTTPException

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email,
                          cognito_username=user.cognito_username,
                          username=user.username,
                          first_name=user.first_name,
                          last_name=user.last_name,
                          birth_date=user.birth_date)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "User created successfully"}

def get_user(db: Session, id: str):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

def get_user_id_by_cognito_username(db: Session, cognito_username: str):
    db_user = db.query(models.User).filter(models.User.cognito_username == cognito_username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user.id

def edit_user(db: Session, id: str, user: schemas.UserEdit):
    db_user = db.query(models.User).filter(models.User.id == id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.email is not None:
        if user.email == db_user.email:
            raise HTTPException(status_code=400, detail="Email is the same")
        
        db_test = db.query(models.User).filter(models.User.email == user.email).first()
        if db_test is not None:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        db_user.email = user.email

    if user.username is not None:
        if user.username == db_user.username:
            raise HTTPException(status_code=400, detail="Username is the same")
        
        db_test = db.query(models.User).filter(models.User.username == user.username).first()
        if db_test is not None:
            raise HTTPException(status_code=400, detail="Username already taken")
        
        db_user.username = user.username

    if user.password is not None: # to be implemented in cognito
        pass

    if user.first_name is not None:
        db_user.first_name = user.first_name

    if user.last_name is not None:
        db_user.last_name = user.last_name

    if user.image_url is not None:
        db_user.image_url = user.image_url

    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_user

# remove method shouldn't be literally deleting the user from the database, just set the user's status to inactive
def remove_user():
    pass