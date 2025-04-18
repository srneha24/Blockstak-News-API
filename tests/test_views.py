import json
from unittest.mock import patch, AsyncMock

import pytest

from views import (
    get_news_view,
    save_latest_news_view,
    get_headlines_by_country_view,
    get_headlines_by_source_view,
    get_headlines_by_filter_view,
)
from schemas import AllowedCountryCodes
from models import Article


@pytest.mark.asyncio
@patch("views.NewsAPI")
async def test_get_news_view(mock_news_api_class, mock_news_api_response):
    """Test the get_news_view function."""
    # Create a mock API instance with async methods
    mock_api = AsyncMock()
    mock_api.get_all_news.return_value = mock_news_api_response
    mock_news_api_class.return_value = mock_api

    # Call the view
    response = await get_news_view(search="test", page=1, limit=10)
    assert response.status_code == 200

    # Parse and verify response
    body = json.loads(response.body)
    assert body["success"] is True
    assert isinstance(body["data"], list)  # API returns articles directly as a list
    assert len(body["data"]) > 0

    # Verify API was called correctly
    mock_api.get_all_news.assert_awaited_once_with(search="test", page=1, limit=10)


@pytest.mark.asyncio
@patch("views.NewsAPI")
async def test_save_latest_news_view(
    mock_news_api_class, mock_news_api_response, test_db
):
    """Test the save_latest_news_view function."""
    # Create mock API instance with async methods
    mock_api = AsyncMock()
    mock_api.get_top_three_headlines.return_value = mock_news_api_response["articles"][
        :3
    ]
    mock_news_api_class.return_value = mock_api

    # Call the view
    response = await save_latest_news_view()
    assert response.status_code == 200

    # Parse and verify response
    body = json.loads(response.body)
    assert body["success"] is True
    assert isinstance(body["data"], list)
    assert len(body["data"]) <= 3

    # Verify API was called
    mock_api.get_top_three_headlines.assert_awaited_once()

    # Verify articles were saved
    saved_articles = await Article.all()
    assert len(saved_articles) > 0


@pytest.mark.asyncio
@patch("views.NewsAPI")
async def test_get_headlines_by_country_view(
    mock_news_api_class, mock_news_api_response
):
    """Test the get_headlines_by_country_view function."""
    # Create mock API instance with async methods
    mock_api = AsyncMock()
    mock_api.get_headlines_by_country.return_value = mock_news_api_response["articles"]
    mock_news_api_class.return_value = mock_api

    # Call the view
    response = await get_headlines_by_country_view(country_code=AllowedCountryCodes.US)
    assert response.status_code == 200

    # Parse and verify response
    body = json.loads(response.body)
    assert body["success"] is True
    assert isinstance(body["data"], list)

    # Verify API was called correctly
    mock_api.get_headlines_by_country.assert_awaited_once_with(
        country_code=AllowedCountryCodes.US
    )


@pytest.mark.asyncio
@patch("views.NewsAPI")
async def test_get_headlines_by_source_view(
    mock_news_api_class, mock_news_api_response
):
    """Test the get_headlines_by_source_view function."""
    # Create mock API instance with async methods
    mock_api = AsyncMock()
    mock_api.get_headlines_by_source.return_value = mock_news_api_response["articles"]
    mock_news_api_class.return_value = mock_api

    # Call the view
    response = await get_headlines_by_source_view(source_id="test-source")
    assert response.status_code == 200

    # Parse and verify response
    body = json.loads(response.body)
    assert body["success"] is True
    assert isinstance(body["data"], list)

    # Verify API was called correctly
    mock_api.get_headlines_by_source.assert_awaited_once_with(source_id="test-source")


@pytest.mark.asyncio
@patch("views.NewsAPI")
async def test_get_headlines_by_filter_view(
    mock_news_api_class, mock_news_api_response
):
    """Test the get_headlines_by_filter_view function."""
    # Create mock API instance with async methods
    mock_api = AsyncMock()
    mock_api.get_headlines_by_country.return_value = mock_news_api_response["articles"]
    mock_api.get_headlines_by_source.return_value = mock_news_api_response["articles"]
    mock_news_api_class.return_value = mock_api

    # Test with both country and source
    response = await get_headlines_by_filter_view(
        country_code=AllowedCountryCodes.US, source_id="test-source"
    )
    assert response.status_code == 200
    body = json.loads(response.body)
    assert body["success"] is True
    assert isinstance(body["data"], list)

    # Test with only country
    response = await get_headlines_by_filter_view(country_code=AllowedCountryCodes.US)
    assert response.status_code == 200
    assert json.loads(response.body)["success"] is True

    # Test with only source
    response = await get_headlines_by_filter_view(source_id="test-source")
    assert response.status_code == 200
    assert json.loads(response.body)["success"] is True

    # Test with no parameters
    response = await get_headlines_by_filter_view()
    assert response.status_code == 400
    body = json.loads(response.body)
    assert body["success"] is False
    assert "country or source" in body["message"].lower()


@pytest.mark.asyncio
@patch("views.NewsAPI")
async def test_get_news_view_failure(mock_news_api_class):
    """Test the get_news_view function when API fails."""
    # Create mock API instance with async methods
    mock_api = AsyncMock()
    mock_api.get_all_news.return_value = None  # API returns None on failure
    mock_news_api_class.return_value = mock_api

    response = await get_news_view(search="test", page=1, limit=10)
    assert response.status_code == 400  # Application returns 400 for API failures
    body = json.loads(response.body)
    assert "Failed to fetch" in body["message"]


@pytest.mark.asyncio
@patch("views.NewsAPI")
async def test_save_latest_news_view_failure(mock_news_api_class, test_db):
    """Test the save_latest_news_view function when API fails."""
    # Create mock API instance with async methods
    mock_api = AsyncMock()
    mock_api.get_top_three_headlines.return_value = None  # API returns None on failure
    mock_news_api_class.return_value = mock_api

    response = await save_latest_news_view()
    assert response.status_code == 400  # Application returns 400 for API failures
    body = json.loads(response.body)
    assert "Failed to fetch" in body["message"]


@pytest.mark.asyncio
@patch("views.NewsAPI")
async def test_get_headlines_by_country_view_failure(mock_news_api_class):
    """Test the get_headlines_by_country_view function when API fails."""
    # Create mock API instance with async methods
    mock_api = AsyncMock()
    mock_api.get_headlines_by_country.return_value = None  # API returns None on failure
    mock_news_api_class.return_value = mock_api

    response = await get_headlines_by_country_view(country_code=AllowedCountryCodes.US)
    assert response.status_code == 400  # Application returns 400 for API failures
    body = json.loads(response.body)
    assert "Failed to fetch" in body["message"]
