from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from apps.api.api_v1.deps import get_db
from apps.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    change_password,
    create_access_token,
    get_current_active_user,
    get_current_user,
    get_password_hash,
)
from apps.crud import user_crud
from apps.schemas.user_schemas import ChangePassword, UserCreateSchema, UserSchema
from apps.services.username_validation import username_slugify

router = APIRouter()


@router.post("/login/access-token")
async def login_for_access_token(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username},
                                       expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/sign-up", response_model=UserSchema)
async def sign_up(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_username(db, user_data.username)
    email = user_crud.get_user_by_email(db, user_data.email)

    if email:
        raise HTTPException(status_code=409, detail="Email exist")

    if user:
        raise HTTPException(
            status_code=409,
            detail="username exist",
        )
    get_password_hash
    user_data.username = username_slugify(user_data.username)
    hashed_password = get_password_hash(user_data.password)

    new_user = user_crud.add_user(db,
                                  user_data,
                                  hashed_password=hashed_password)
    return new_user


@router.get("/me", response_model=UserSchema)
async def read_users_me(
        current_user: UserSchema = Depends(get_current_active_user)):
    return current_user


@router.post("/reset-password/{username:str}")
async def reset_password(username: str,
                         data_user: ChangePassword,
                         db: Session = Depends(get_db)):
    user = user_crud.get_user_by_username(db=db, username=username)
    if not user.username:
        raise HTTPException(status_code=409, detail="username no exist")
    if data_user.new_password != data_user.confirm_password:
        raise HTTPException(status_code=409, detail="different password")

    user = change_password(data_user=data_user, db=db, user=user)
    db.add(user)
    db.commit()
    return {"detail": "Password updated successfully"}
