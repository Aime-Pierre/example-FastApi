from sqlmodel import create_engine, Session
from .config import settings

# Connection to the postgresql database
DATABASE_URL =f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session






