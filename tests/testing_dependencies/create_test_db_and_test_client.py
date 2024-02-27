from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from service.dependencies import get_db
from persistence.sqlite_db import Base
from fastapi.testclient import TestClient
from main import app


# Create test client
client = TestClient(app)


#  Create test database
SQLALCHEMY_DATABASE_URL = 'sqlite://'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override test client with test db
app.dependency_overrides[get_db] = override_get_db
