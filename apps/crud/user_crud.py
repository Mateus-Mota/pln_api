from typing import List, Optional

from sqlalchemy.orm import Session

from apps.models.user_models import UserModel
from apps.schemas.user_schemas import ChangePassword, UserCreateSchema, UserSchema


def get_all_users(db: Session) -> List[UserModel]:
    return db.query(UserModel).filter().all()


def get_user_by_username(db: Session, username: str) -> Optional[UserModel]:
    return db.query(UserModel).filter(UserModel.username == username).first()


def get_user_by_email(db: Session, email: str) -> UserModel:
    return db.query(UserModel).filter(
        UserModel.email == email).first()  # type: ignore


def add_user(db: Session, user_data: UserCreateSchema,
             hashed_password) -> UserSchema:

    db_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, email: str):
    db.delete(email=email)  # type: ignore
    db.commit()
