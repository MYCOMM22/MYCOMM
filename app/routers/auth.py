from fastapi import  Depends, FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database , schemas, models,utils, oauth2

router = APIRouter(tags=["Authentication"])


@router.post('/login',response_model=schemas.Token)
def login(user_cred : OAuth2PasswordRequestForm = Depends() , db: Session = Depends(database.get_db)):
    user = db.query(models.admin).filter(models.admin.phone == user_cred.username).first()

    if not user :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "invalid")

    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="wrong password")

    access_token=oauth2.create_access_token_admin(data = {"user_id":user.id})
    return {"access_token": access_token, "token_type":"Bearer"}

@router.post('/slogin',response_model=schemas.Token)
def login(user_cred : OAuth2PasswordRequestForm = Depends() , db: Session = Depends(database.get_db)):
    user = db.query(models.subadmin).filter(models.subadmin.phone == user_cred.username).first()

    if not user :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "invalid")

    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="wrong password")

    access_token=oauth2.create_access_token_subadmin(data = {"user_id":user.id})
    return {"access_token": access_token, "token_type":"Bearer"}

@router.post('/ulogin',response_model=schemas.Token)
def login(user_cred : OAuth2PasswordRequestForm = Depends() , db: Session = Depends(database.get_db)):
    user = db.query(models.user).filter(models.user.phone == user_cred.username).first()

    if not user :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "invalid")

    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="wrong password")

    access_token=oauth2.create_access_token_user(data = {"user_id":user.id})
    return {"access_token": access_token, "token_type":"Bearer"}

    