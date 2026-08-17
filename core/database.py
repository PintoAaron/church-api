from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core import envConfig

DATABASE_URL = f"postgresql://{envConfig.POSTGRES_USER}:{envConfig.POSTGRES_PASSWORD}@{envConfig.POSTGRES_HOST}:{envConfig.POSTGRES_PORT}/{envConfig.POSTGRES_DB}"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def get_db_session():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
