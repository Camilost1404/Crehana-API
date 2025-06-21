from sqlmodel import Session, SQLModel, create_engine

from app.core.settings import settings

DATABASE_URL = settings.database_url
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=True,  # Set to True for SQL query logging
)


def get_db():
    """
    Dependency to get the database engine.
    This can be used in FastAPI routes to access the database.
    """
    with Session(engine) as session:
        yield session


def init_db():
    """
    Initialize the database by creating all tables.
    This should be called at application startup.
    """
    # TODO: Import your models here to ensure they are registered with SQLModel
    SQLModel.metadata.create_all(engine)
