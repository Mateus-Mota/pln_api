from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from apps.core.config import get_settings
from apps.db.database import Base, get_db
from apps.main import app

settings = get_settings()

# docker run --name postgres  -e "POSTGRES_PASSWORD=1234" -p 5432:5432 -d postgres:13
# db url test
SQLALCHEMY_DATABASE_URL = settings.DATABASE_TEST_URI

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
