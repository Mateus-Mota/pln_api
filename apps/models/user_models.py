import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from apps.db.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class UserModel(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    username = Column(String(20), unique=True, index=True, nullable=False)
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String)

    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def full_name(self):
        return self.first_name + " " + self.last_name
