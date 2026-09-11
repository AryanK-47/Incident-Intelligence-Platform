from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase,session
from app.core.config import settings


database_url = (
    f"postgresql+psycopg://"
    f"{settings.user}:{settings.password}"
    f"@{settings.host}:{settings.port}"
    f"/{settings.dbname}"
    f"?sslmode=require"
)
engine=create_engine(database_url)

class Base(DeclarativeBase):
    pass

SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)


def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()
    
