from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserSchema(UserBase):
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class UserResponseSchema(UserBase):
    first_name: str
    last_name: str
    username: str

    class Config:
        orm_mode = True


class UserCreateSchema(UserSchema):
    password: str
    username: str

    class Config:
        orm_mode = False


class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    class Config:
        orm_mode = False
