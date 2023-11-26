from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.database import get_db
from main import app

def postgres_container():
    container = PostgresContainer("postgres:latest")
    container.start()
    print(container.get_connection_url())
    yield container
    container.stop()

container = next(postgres_container())
engine = create_engine(container.get_connection_url())

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


