from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from apps.api.api_v1.api import api_router
from apps.api.api_v1.endpoints import accuracy
from apps.models import accuracy_models, user_models

from .db.database import Base, SessionLocal, engine

app = FastAPI(openapi_url="/openapi.json", debug=True)

# Base.metadata.drop_all(bind=engine, tables=[
#    accuracy_models.AccuracyModel.__table__])
# Base.metadata.drop_all(bind=engine, tables=[user_models.UserModel.__table__])

accuracy_models.Base.metadata.create_all(bind=engine)
user_models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080"
    "http://0.0.0.0:8000/",
    "http://0.0.0.0"
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# prefix and version api
app.router.prefix = "/api/v1"

app.include_router(api_router)

# uvicorn apps.main:app --reload
# uvicorn apps.main:app --reload --workers 1 --host 0.0.0.0 --port 8090
# docker-compose exec db psql --username=postgres --dbname=app
