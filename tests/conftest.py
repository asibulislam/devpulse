import pytest
import os
import itertools
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

TEST_DB_URL = "sqlite:///./test_devpulse.db"

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

_counter = itertools.count(1)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test_devpulse.db"):
        os.remove("test_devpulse.db")


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


def unique_username():
    return f"testuser_{next(_counter)}"


def register_user(client, username, password="testpass123"):
    return client.post("/api/auth/register", data={
        "username": username,
        "password": password
    })


def get_token(client, username, password="testpass123"):
    response = client.post("/api/auth/login", data={
        "username": username,
        "password": password
    })
    return response.json()["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}