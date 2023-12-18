from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from main import app

# Use the environment variables from the .env file for your test database
TEST_POSTGRES_DB = "test_db"
TEST_POSTGRES_USER = "test_user"
TEST_POSTGRES_PASSWORD = "test_password"
TEST_POSTGRES_HOST = "localhost"
TEST_POSTGRES_PORT = "5430"

# Define the TEST PostgreSQL connection URL
TEST_SQLALCHEMY_DATABASE_URL = f"postgresql://{TEST_POSTGRES_USER}:{TEST_POSTGRES_PASSWORD}@{TEST_POSTGRES_HOST}:{TEST_POSTGRES_PORT}/{TEST_POSTGRES_DB}"

test_engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

from app.database import Base, get_db

Base.metadata.create_all(bind=test_engine)


def get_test_db():
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = get_test_db