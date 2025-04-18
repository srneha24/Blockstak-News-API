from datetime import datetime, timedelta
from unittest.mock import patch

import jwt
from fastapi.testclient import TestClient

from conf.vars import JWT_SECRET, CLIENT_ID
from utils.token import generate_access_token


def test_get_code(test_app: TestClient):
    """Test the code generation endpoint."""
    response = test_app.get("/code", params={"client_id": "test-client"})
    assert response.status_code == 200
    assert "code" in response.json()["data"]
    assert isinstance(response.json()["data"]["code"], str)


def test_get_token_valid_credentials(test_app: TestClient):
    """Test token generation with valid credentials."""
    # First get a code
    response = test_app.get("/code", params={"client_id": "demo-client"})
    code = response.json()["data"]["code"]
    # Then get a token
    response = test_app.get(
        "/token",
        params={
            "client_id": "demo-client",
            "client_secret": "C51D80D50A15DF7D",
            "code": code,
        },
    )
    assert response.status_code == 200
    assert "token" in response.json()["data"]
    # Verify the token
    token = response.json()["data"]["token"]
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    assert payload["sub"] == CLIENT_ID


def test_get_token_invalid_code(test_app: TestClient):
    """Test token generation with invalid code."""
    response = test_app.get(
        "/token",
        params={
            "client_id": "demo-client",
            "client_secret": "C51D80D50A15DF7D",
            "code": "invalid-code",
        },
    )
    assert response.status_code == 400
    assert "Invalid Code" in response.json()["message"]


def test_get_token_invalid_client(test_app: TestClient):
    """Test token generation with invalid client credentials."""
    response = test_app.get(
        "/token",
        params={
            "client_id": "invalid-client",
            "client_secret": "invalid-secret",
            "code": "some-code",
        },
    )
    assert response.status_code == 400
    assert "Client Not Found" in response.json()["message"]


@patch("utils.token.datetime")
def test_token_generation(mock_datetime):
    """Test the token generation utility."""
    # Mock the current time to a fixed known value
    current_time = datetime(2025, 4, 18, 12, 0, 0)
    mock_datetime.now.return_value = current_time
    token = generate_access_token()
    payload = jwt.decode(
        token, JWT_SECRET, algorithms=["HS256"], options={"verify_exp": False}
    )
    assert payload["sub"] == CLIENT_ID
    # Verify expiration is set correctly (30 minutes from current time)
    expected_exp = (current_time + timedelta(minutes=30)).timestamp()
    assert abs(payload["exp"] - expected_exp) < 1  # Allow 1 second difference
