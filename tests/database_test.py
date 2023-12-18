from app.database import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.postgres import PostgresContainer

# Use the environment variables from the .env file for your test database
TEST_POSTGRES_DB = "test_db"
TEST_POSTGRES_USER = "test_user"
TEST_POSTGRES_PASSWORD = "test_password"
TEST_POSTGRES_PORT = "5432"

# Create a test database container
postgres_container = PostgresContainer("postgres:13.2-alpine",
                                       dbname=TEST_POSTGRES_DB,
                                       user=TEST_POSTGRES_USER,
                                       password=TEST_POSTGRES_PASSWORD,
                                       port=TEST_POSTGRES_PORT)

# Start the container
postgres_container.start()

# Wait for the container to start
wait_for_logs(postgres_container, "database system is ready to accept connections")

# Get the host port
postgres_port = postgres_container.get_exposed_port(TEST_POSTGRES_PORT)

# Create the database engine
engine = create_engine(f"postgresql://{TEST_POSTGRES_USER}:{TEST_POSTGRES_PASSWORD}@"
                       f"localhost:{postgres_port}/{TEST_POSTGRES_DB}")

# Create the test database tables
Base.metadata.create_all(bind=engine)

# Create a test database session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a test database session
def get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

