from unittest.mock import patch, MagicMock
from datetime import datetime
from logging import LogRecord

import pytest
import pytz
from newsapi.newsapi_exception import NewsAPIException

from utils.news_api_client import NewsAPI
from utils.log import Log
from conf.log import LocalFormatter, LOGGING_CONFIG


@pytest.mark.asyncio
async def test_get_all_news_success(mock_news_api_response):
    """Test successful news retrieval."""
    mock_client = MagicMock()
    mock_client.get_everything.return_value = mock_news_api_response

    news_api = NewsAPI()
    news_api.client = mock_client
    await news_api.get_all_news(search="test", page=1, limit=10)

    # Verify the API was called with correct parameters
    mock_client.get_everything.assert_called_once_with(q="test", page=1, page_size=10)


@pytest.mark.asyncio
async def test_get_all_news_failure():
    """Test news retrieval with API error."""
    mock_client = MagicMock()
    mock_client.get_everything.side_effect = NewsAPIException("API Error")

    news_api = NewsAPI()
    news_api.client = mock_client
    result = await news_api.get_all_news(search="test", page=1, limit=10)
    assert result is None


@pytest.mark.asyncio
async def test_get_top_three_headlines_success(mock_news_api_response):
    """Test successful retrieval of top headlines."""
    mock_client = MagicMock()
    mock_client.get_top_headlines.return_value = mock_news_api_response

    news_api = NewsAPI()
    news_api.client = mock_client
    await news_api.get_top_three_headlines()

    mock_client.get_top_headlines.assert_called_once_with(
        country="us", page=1, page_size=5
    )


@pytest.mark.asyncio
async def test_get_headlines_by_country_success(mock_news_api_response):
    """Test successful retrieval of headlines by country."""
    mock_client = MagicMock()
    mock_client.get_top_headlines.return_value = mock_news_api_response

    news_api = NewsAPI()
    news_api.client = mock_client
    await news_api.get_headlines_by_country(country_code="us")

    mock_client.get_top_headlines.assert_called_once_with(country="us")


@pytest.mark.asyncio
async def test_get_headlines_by_source_success(mock_news_api_response):
    """Test successful retrieval of headlines by source."""
    mock_client = MagicMock()
    mock_client.get_top_headlines.return_value = mock_news_api_response

    news_api = NewsAPI()
    news_api.client = mock_client
    await news_api.get_headlines_by_source(source_id="bbc-news")

    mock_client.get_top_headlines.assert_called_once_with(sources="bbc-news")


@patch("utils.log.LOGGER")
def test_log_info(mock_logger):
    """Test info level logging."""
    test_message = "Test info message"
    test_data = {"key": "value"}

    Log.info(test_message, test_data)

    mock_logger.info.assert_called_once()
    args, kwargs = mock_logger.info.call_args
    assert test_message in args[0]
    assert "data" in kwargs.get("extra", {})
    assert kwargs["extra"]["data"] == test_data


@patch("utils.log.LOGGER")
def test_log_error(mock_logger):
    """Test error level logging."""
    test_message = "Test error message"
    test_data = {"error": "test error"}

    Log.error(test_message, test_data)

    mock_logger.error.assert_called_once()
    args, kwargs = mock_logger.error.call_args
    assert test_message in args[0]
    assert "data" in kwargs.get("extra", {})
    assert kwargs["extra"]["data"] == test_data


@patch("utils.log.LOGGER")
def test_log_warning(mock_logger):
    """Test warning level logging."""
    test_message = "Test warning message"
    test_data = {"warning": "test warning"}

    Log.warning(test_message, test_data)

    mock_logger.warning.assert_called_once()
    args, kwargs = mock_logger.warning.call_args
    assert test_message in args[0]
    assert "data" in kwargs.get("extra", {})
    assert kwargs["extra"]["data"] == test_data


def test_local_formatter():
    """Test the custom LocalFormatter."""
    formatter = LocalFormatter()

    # Create a proper LogRecord instance
    record = LogRecord(
        name="test_logger",
        level=20,  # INFO level
        pathname=__file__,
        lineno=1,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    record.created = datetime.now(pytz.UTC).timestamp()
    record.msecs = 0
    record.levelname = "INFO"
    record.data = {"key": "value"}

    # Create a formatted message
    formatted = formatter.format(record)

    # Verify the formatted message contains all required parts
    assert "INFO" in formatted
    assert "Test message" in formatted
    assert "{'key': 'value'}" in formatted
    assert datetime.now().strftime("%Y") in formatted


@patch("utils.log.LOGGER")
def test_log_method_info_capture(mock_logger):
    """Test that log captures method information correctly."""

    def test_function():
        Log.info("Test message")

    test_function()

    mock_logger.info.assert_called_once()
    _, kwargs = mock_logger.info.call_args
    assert "method_info" in kwargs.get("extra", {})
    method_info = kwargs["extra"]["method_info"]
    assert "test_function" in method_info["method"]
    assert __file__ in method_info["file_path"]


def test_logging_config_structure():
    """Test the logging configuration structure."""
    assert "version" in LOGGING_CONFIG
    assert "formatters" in LOGGING_CONFIG
    assert "handlers" in LOGGING_CONFIG
    assert "loggers" in LOGGING_CONFIG

    assert "local" in LOGGING_CONFIG["formatters"]
    assert "default_formatter" in LOGGING_CONFIG["formatters"]

    assert "stream_handler" in LOGGING_CONFIG["handlers"]
    assert "console" in LOGGING_CONFIG["handlers"]
    assert "local" in LOGGING_CONFIG["handlers"]
