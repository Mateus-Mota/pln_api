import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, column
from sqlalchemy.dialects.postgresql import UUID

from apps.db.database import Base


class AccuracyModel(Base):
    __tablename__ = "accuracys"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    accuracy = Column(Float)
    message = Column(String)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
