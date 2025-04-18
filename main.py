import hashlib
import random
import string
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware import Middleware
from tortoise.contrib.fastapi import register_tortoise
from pydantic import ValidationError
from cachetools import TTLCache

from conf.database import TORTOISE_CONFIG
from conf.middlewares import AuthenticationMiddleware
from conf.response import (
    custom_request_validation_exception_handler,
    custom_http_exception_handler,
    CustomJSONResponse,
    custom_validation_error_handler,
)
from utils.token import generate_access_token
from routers import router as news_router


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(AuthenticationMiddleware),
]


async def not_found(_request, _exc):
    """Custom handler for 404 errors."""
    return PlainTextResponse(content="Page Not Found!", status_code=404)


exceptions = {
    404: not_found,
}


app = FastAPI(middleware=middleware, exception_handlers=exceptions)
app.include_router(news_router)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request, exc):
    """Custom handler for request validation exceptions."""
    return await custom_request_validation_exception_handler(request, exc)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom handler for HTTP exceptions."""
    return await custom_http_exception_handler(request, exc)


@app.exception_handler(ValidationError)
async def validator_error_handler(request, exc):
    """Custom handler for validation errors."""
    return await custom_validation_error_handler(request, exc)


@app.exception_handler(Exception)
async def custom_exception_handler(_request, exc):
    """Custom handler for general exceptions."""
    response_data = {"message": "Exception Raised", "details": str(exc)}
    return CustomJSONResponse(content=response_data, status_code=500)


register_tortoise(
    app=app,
    config=TORTOISE_CONFIG,
    generate_schemas=True,
    add_exception_handlers=True,
)

cache = TTLCache(maxsize=5, ttl=300)
DEFAULT_CLIENT_HASH = "6f7517d93cdaaecaa64f3052d135539e"


@app.get("/code")
async def get_code(_request: Request, client_id: str):
    """Endpoint to get a code."""
    length = random.randint(8, 10)
    code = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(length)
    )
    cache[client_id] = code
    return CustomJSONResponse(content={"code": code})


@app.get("/token")
async def get_token(_request: Request, client_id: str, client_secret: str, code: str):
    """Endpoint to get a token."""
    client = f"client_id:{client_id}-client_secret:{client_secret}"
    md5_hash = hashlib.md5()
    md5_hash.update(client.encode('utf-8'))
    client_hash = md5_hash.hexdigest()
    if client_hash != DEFAULT_CLIENT_HASH:
        raise HTTPException(status_code=400, detail="Client Not Found")
    cached_code = cache.get(client_id)
    if not cached_code:
        raise HTTPException(status_code=400, detail="Code Expired")
    if code != cached_code:
        raise HTTPException(status_code=400, detail="Invalid Code")
    access_token = generate_access_token()
    return CustomJSONResponse(content={"token": access_token})
