import asyncio
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from tortoise import Tortoise

from test_config import TEST_DB_CONFIG, MOCK_NEWS_RESPONSE, TEST_VALID_TOKEN
from main import app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    if loop.is_running():
        loop.stop()
    if not loop.is_closed():
        loop.close()


@pytest.fixture(scope="session")
async def initialize_tests(event_loop):
    """Initialize test database and close properly"""
    await Tortoise.init(config=TEST_DB_CONFIG)
    await Tortoise.generate_schemas()

    yield

    await Tortoise.close_connections()


@pytest.fixture(scope="function")
async def test_db(initialize_tests):
    """Create a fresh database connection for each test."""
    connection = Tortoise.get_connection("default")
    await connection.execute_query("DELETE FROM article")  # Clean up before each test

    yield connection

    await connection.execute_query("DELETE FROM article")  # Clean up after each test


@pytest.fixture(scope="session")
def test_app():
    client = TestClient(app)
    return client


@pytest.fixture
def mock_news_api_response():
    return MOCK_NEWS_RESPONSE


@pytest.fixture
def auth_token_headers():
    return {"Authorization": f"Bearer {TEST_VALID_TOKEN}"}


@pytest.fixture
def mock_datetime():
    """Mock datetime to return a fixed time."""

    class MockDateTime:
        @staticmethod
        def now():
            return datetime(2025, 4, 18, 12, 0, 0)

        @staticmethod
        def utcnow():
            return datetime(2025, 4, 18, 12, 0, 0)

    return MockDateTime


@pytest.fixture
def mock_newsapi_client(mocker):
    """Mock NewsAPI client for testing."""
    mock = mocker.patch("newsapi.NewsApiClient")
    mock_instance = mocker.MagicMock()
    mock_instance.get_everything.return_value = MOCK_NEWS_RESPONSE
    mock_instance.get_top_headlines.return_value = MOCK_NEWS_RESPONSE
    mock.return_value = mock_instance
    return mock_instance
