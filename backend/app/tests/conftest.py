# Fixtures and shared test setup
from unittest.mock import AsyncMock, Mock
import httpx
import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.connection import get_db
from app.models.base import Base

# Use SQLite for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Set up async SQLAlchemy session for tests
engine_test = create_async_engine(TEST_DATABASE_URL, future=True)
AsyncSessionTest = sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)


# ✅ Override FastAPI's DB dependency
async def override_get_db():
    async with AsyncSessionTest() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


# ✅ Setup the database once per test session
@pytest.fixture(scope="session")
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine_test.dispose()


# ✅ Reset DB and provide test client per function
@pytest_asyncio.fixture(scope="function")
async def client():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


# ✅ Fixture: returns a unique user payload per test
@pytest_asyncio.fixture
def unique_user_data():
    uid = uuid.uuid4().hex[:8]
    return {
        "username": f"user_{uid}",
        "email": f"user_{uid}@example.com",
        "full_name": "Test User",
        "password": "testpass123",
    }


# ✅ Fixture: returns a different user (useful for other-user logic)
@pytest_asyncio.fixture
def another_user_data():
    uid = uuid.uuid4().hex[:8]
    return {
        "username": f"alt_{uid}",
        "email": f"alt_{uid}@example.com",
        "full_name": "Another User",
        "password": "testpass321",
    }


# ✅ Fixture: logs in and returns auth headers
@pytest_asyncio.fixture
async def auth_headers(client, unique_user_data):
    await client.post("/auth/register", json=unique_user_data)

    login_resp = await client.post(
        "/auth/login",
        data={
            "username": unique_user_data["email"],
            "password": unique_user_data["password"],
        },
    )
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"

    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(autouse=True)
def mock_httpx_async_client(mocker):
    # Patch httpx.AsyncClient (the class itself)
    mock_client_constructor = mocker.patch("httpx.AsyncClient")

    # This mock represents the object returned by `async with AsyncClient() as client`
    mock_client_instance = Mock()

    # Mock .post() with desired fake behavior
    mock_client_instance.post = AsyncMock(side_effect=fake_post)

    # Configure the async context manager behavior
    mock_client_constructor.return_value.__aenter__.return_value = mock_client_instance


# Your fake post logic — customize as needed
async def fake_post(url, *args, **kwargs):
    request = httpx.Request("POST", url)

    if "moderate-text" in url:
        return httpx.Response(
            200, json={"category": "OK", "description": "Clean"}, request=request
        )
    elif "detect-language" in url:
        return httpx.Response(200, json={"language": "English"}, request=request)
    elif "extract-hashtags" in url:
        return httpx.Response(200, json={"hashtags": ["ml", "test"]}, request=request)
    else:
        return httpx.Response(404, json={"detail": "Unknown route"}, request=request)
