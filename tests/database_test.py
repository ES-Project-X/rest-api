from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use the environment variables from the .env file for your test database
TEST_POSTGRES_DB = "test_db"
TEST_POSTGRES_USER = "test_user"
TEST_POSTGRES_PASSWORD = "test_password"
TEST_POSTGRES_HOST = "localhost"
TEST_POSTGRES_PORT = "5432"

# Define the TEST PostgreSQL connection URL
TEST_SQLALCHEMY_DATABASE_URL = f"postgresql://{TEST_POSTGRES_USER}:{TEST_POSTGRES_PASSWORD}@{TEST_POSTGRES_HOST}:{TEST_POSTGRES_PORT}/{TEST_POSTGRES_DB}"

test_engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

TestBase = declarative_base()

def get_test_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
