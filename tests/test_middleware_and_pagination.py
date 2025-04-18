from unittest.mock import MagicMock, patch

import pytest
import jwt
from fastapi import Request, HTTPException

from conf.middlewares import AuthenticationMiddleware
from conf.permissions import IsAuthenticated
from conf.paginations import Pagination
from conf.vars import CLIENT_ID


@pytest.mark.asyncio
@patch("jwt.decode")
async def test_authentication_middleware(mock_jwt_decode):
    """Test the authentication middleware."""
    middleware = AuthenticationMiddleware(app=None)

    # Configure mock to return valid payload
    mock_jwt_decode.return_value = {"sub": CLIENT_ID}

    # Test with valid token
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"authorization": "Bearer valid-token"}
    mock_request.state = MagicMock()

    async def mock_call_next(_):
        return MagicMock()

    response = await middleware.dispatch(mock_request, mock_call_next)
    assert response is not None
    assert mock_request.state.is_authenticated is True

    # Test with invalid token
    mock_jwt_decode.side_effect = jwt.InvalidTokenError()
    mock_request.headers = {"authorization": "Bearer invalid-token"}
    response = await middleware.dispatch(mock_request, mock_call_next)
    assert response is not None
    assert mock_request.state.is_authenticated is False

    # Test without token
    mock_request.headers = {}
    response = await middleware.dispatch(mock_request, mock_call_next)
    assert response is not None
    assert mock_request.state.is_authenticated is False


@pytest.mark.asyncio
async def test_authentication_middleware_with_expired_token():
    """Test the authentication middleware with an expired token."""
    middleware = AuthenticationMiddleware(app=None)

    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"authorization": "Bearer expired.token.here"}
    mock_request.state = MagicMock()

    async def mock_call_next(_):
        return MagicMock()

    with patch("jwt.decode", side_effect=jwt.ExpiredSignatureError):
        response = await middleware.dispatch(mock_request, mock_call_next)
        assert response is not None
        assert mock_request.state.is_authenticated is False


@pytest.mark.asyncio
async def test_authentication_middleware_with_invalid_token_format():
    """Test the authentication middleware with invalid token format."""
    middleware = AuthenticationMiddleware(app=None)

    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"authorization": "InvalidFormat token"}
    mock_request.state = MagicMock()

    async def mock_call_next(_):
        return MagicMock()

    response = await middleware.dispatch(mock_request, mock_call_next)
    assert response is not None
    assert mock_request.state.is_authenticated is False


@pytest.mark.asyncio
async def test_is_authenticated_permission():
    """Test the IsAuthenticated permission class."""
    permission = IsAuthenticated()

    # Test with authenticated request
    mock_request = MagicMock(spec=Request)
    mock_request.state.is_authenticated = True
    result = await permission(mock_request)
    assert result is None

    # Test with unauthenticated request
    mock_request.state.is_authenticated = False
    with pytest.raises(HTTPException) as exc:
        await permission(mock_request)
    assert exc.value.status_code == 401
    assert "Authentication Failed" in exc.value.detail


def test_pagination():
    """Test the pagination functionality."""
    # Test with data
    data = [{"id": i, "value": f"test{i}"} for i in range(5)]
    pagination = Pagination(page=1, limit=2, total_count=5, data=data[:2])

    paginated_data = pagination.get_paginated_data()
    assert paginated_data["totalCount"] == 5
    assert paginated_data["page"] == 1
    assert paginated_data["limit"] == 2
    assert paginated_data["nextPage"] == 2
    assert paginated_data["prevPage"] is None
    assert paginated_data["pageCount"] == 3
    assert len(paginated_data["data"]) == 2

    # Test last page
    pagination = Pagination(page=3, limit=2, total_count=5, data=data[4:])
    paginated_data = pagination.get_paginated_data()
    assert paginated_data["nextPage"] is None
    assert paginated_data["prevPage"] == 2

    # Test middle page
    pagination = Pagination(page=2, limit=2, total_count=5, data=data[2:4])
    paginated_data = pagination.get_paginated_data()
    assert paginated_data["nextPage"] == 3
    assert paginated_data["prevPage"] == 1

    # Test with empty data
    pagination = Pagination(page=1, limit=2, total_count=0, data=[])
    paginated_data = pagination.get_paginated_data()
    assert paginated_data["totalCount"] == 0
    assert paginated_data["nextPage"] is None
    assert paginated_data["prevPage"] is None
    assert paginated_data["pageCount"] == 0
    assert len(paginated_data["data"]) == 0
