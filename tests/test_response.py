import json

import pytest
from pydantic import BaseModel, ValidationError

from conf.response import CustomJSONResponse, custom_validation_error_handler


def test_custom_json_response_success():
    """Test successful response formatting."""
    data = {"key": "value"}
    response = CustomJSONResponse(content=data)
    assert response.status_code == 200

    # Need to decode and parse the response body
    body = json.loads(response.body)
    assert body["success"] is True
    assert body["message"] == "Request Success"
    assert body["data"] == data


def test_custom_json_response_failure():
    """Test failure response formatting."""
    data = {"error": "test error"}
    response = CustomJSONResponse(content=data, status_code=400)
    assert response.status_code == 400

    body = json.loads(response.body)
    assert body["success"] is False
    assert body["message"] == "Request Failed"
    assert body["data"] == data


def test_custom_json_response_with_message():
    """Test response formatting with custom message."""
    data = {"key": "value"}
    message = "Custom message"
    response = CustomJSONResponse(content=data, message=message)

    body = json.loads(response.body)
    assert body["message"] == message


def test_custom_json_response_with_nested_message():
    """Test response formatting with message in data."""
    data = {"data": {"message": "Nested message"}}
    response = CustomJSONResponse(content=data)

    body = json.loads(response.body)
    assert body["message"] == "Nested message"


@pytest.mark.asyncio
async def test_validation_error_handler():
    """Test handling of Pydantic validation errors."""

    class TestModel(BaseModel):
        name: str
        age: int

    try:
        TestModel(name=123, age="invalid")
    except ValidationError as e:
        response = await custom_validation_error_handler(None, e)
        assert response.status_code == 400

        body = json.loads(response.body)
        assert body["success"] is False
        assert "Validation Error" in body["message"]
        assert "detail" in body
