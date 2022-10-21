from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from apps.api.api_v1.deps import get_db
from apps.core.config import get_settings
from apps.crud import user_crud
from apps.models.user_models import UserModel
from apps.schemas.token_schemas import TokenDataSchema
from apps.schemas.user_schemas import ChangePassword

settings = get_settings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    user: UserModel = user_crud.get_user_by_username(
        db=db, username=username)  # type: ignore
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: Session = Depends(get_db)) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # type: ignore
        if username is None:
            raise credentials_exception
        token_data = TokenDataSchema(username=username)
    except JWTError:
        raise credentials_exception
    user = user_crud.get_user_by_username(
        db, username=token_data.username)  # type: ignore
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_user_is_admin(
        current: UserModel = Depends(get_current_active_user), ):
    if not current.is_admin:
        raise HTTPException(status_code=400, detail="User no adm")


def change_password(data_user: ChangePassword, db: Session, user):

    if verify_password(data_user.current_password, user.hashed_password):
        hashed_password = get_password_hash(data_user.new_password)
        user.hashed_password = hashed_password
        return user
