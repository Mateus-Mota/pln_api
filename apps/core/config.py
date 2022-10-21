from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "API PLN"

    VOCAB_FNAME: str = "apps/pln/services/ttVocab"
    PATH_MY_WEIGHTS: str = "apps/pln/weights_folder/my_weights"
    TRAIN_CSV: str = "apps/pln/data/trainingandtestdata/train.csv"
    TEST_CSV: str = "apps/pln/data/trainingandtestdata/test.csv"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str

    DATABASE_URI: str
    DATABASE_TEST_URI: str
    # initial
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_NAME: str
    FIRST_LAST_NAME: str
    FIRST_EMAIL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    LOCAL_REDIS_URL: str = "redis://redis:6379"

    class Config:
        case_sensitive = True
        env_prefix = ""
        env_file = "../.env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings(_env_file=".env", _env_file_encoding="utf-8")
