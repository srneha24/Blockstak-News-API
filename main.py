import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware import Middleware
from tortoise.contrib.fastapi import register_tortoise
from pydantic import ValidationError

from conf.vars import CLIENT_SECRET
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
from schemas import Client


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


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Create the log directory if it doesn't exist
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(BASE_DIR, "logs")
    os.makedirs(log_dir, exist_ok=True)

    yield

    pass


app = FastAPI(middleware=middleware, lifespan=lifespan, exception_handlers=exceptions)
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


@app.post("/token")
async def get_token(_request: Request, payload: Client):
    """Endpoint to get a token."""
    if payload.client_secret != CLIENT_SECRET:
        raise HTTPException(status_code=400, detail="Client Not Found")
    return CustomJSONResponse(content={"token": generate_access_token()})
