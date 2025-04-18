import pytest
import jwt
from fastapi.testclient import TestClient
from tortoise import Tortoise

from test_config import TEST_DB_CONFIG
from main import app
from conf.vars import JWT_SECRET, CLIENT_ID


@pytest.fixture(scope="module", autouse=True)
async def setup_test_database():
    """Set up test database for integration tests."""
    await Tortoise.init(config=TEST_DB_CONFIG)
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest.fixture
def api_client():
    """Get test client with proper database setup."""
    with TestClient(app) as client:
        yield client


@pytest.mark.asyncio
async def test_full_auth_flow(api_client: TestClient):
    """Test the complete authentication flow."""
    # Step 1: Get code
    response = api_client.get("/code", params={"client_id": "demo-client"})
    assert response.status_code == 200
    code = response.json()["data"]["code"]
    assert code is not None

    # Step 2: Get token
    response = api_client.get(
        "/token",
        params={
            "client_id": "demo-client",
            "client_secret": "C51D80D50A15DF7D",
            "code": code,
        },
    )
    assert response.status_code == 200
    token = response.json()["data"]["token"]
    assert token is not None

    # Verify token
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    assert payload["sub"] == CLIENT_ID


@pytest.mark.asyncio
async def test_authenticated_news_flow(api_client: TestClient):
    """Test the complete news API flow with authentication."""
    # First get a valid token
    response = api_client.get("/code", params={"client_id": "demo-client"})
    code = response.json()["data"]["code"]
    response = api_client.get(
        "/token",
        params={
            "client_id": "demo-client",
            "client_secret": "C51D80D50A15DF7D",
            "code": code,
        },
    )
    token = response.json()["data"]["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test news search
    response = api_client.get(
        "/news", params={"search": "test", "page": 1, "limit": 10}, headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "totalCount" in data
    assert "page" in data
    assert "limit" in data

    # Test save latest news
    response = api_client.post("/news/save-latest", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) <= 3

    # Test headlines by country
    response = api_client.get("/news/headlines/country/us", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data

    # Test headlines by source
    response = api_client.get("/news/headlines/source/bbc-news", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data

    # Test headlines filter
    response = api_client.get(
        "/news/headlines/filter",
        params={"country": "us", "source": "bbc-news"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data


@pytest.mark.asyncio
async def test_error_cases(api_client: TestClient):
    """Test various error cases in the API flow."""
    # Invalid client credentials
    response = api_client.get(
        "/token",
        params={"client_id": "wrong", "client_secret": "wrong", "code": "wrong"},
    )
    assert response.status_code == 400
    assert "Client Not Found" in response.json()["message"]

    # Missing authentication
    response = api_client.get(
        "/news", params={"search": "test", "page": 1, "limit": 10}
    )
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["message"]

    # Invalid country code
    response = api_client.get(
        "/news/headlines/country/invalid",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code in [400, 401, 422]  # Either auth or validation error

    # Missing required parameters
    response = api_client.get(
        "/news", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code in [400, 401, 422]  # Either auth or validation error
