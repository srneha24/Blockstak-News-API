from fastapi import FastAPI, HTTPException, Request, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware import Middleware
from tortoise.contrib.fastapi import register_tortoise
from pydantic import ValidationError

from conf.log import LOG_DIR
from conf.database import TORTOISE_CONFIG
from conf.response import (
    custom_request_validation_exception_handler,
    custom_http_exception_handler,
    CustomJSONResponse,
    custom_validation_error_handler,
)


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]


async def not_found(request, exc):
    """Custom handler for 404 errors."""
    return PlainTextResponse(content="Page Not Found!", status_code=404)


exceptions = {
    404: not_found,
}


app = FastAPI(middleware=middleware, exception_handlers=exceptions)


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
async def custom_exception_handler(request, exc):
    """Custom handler for general exceptions."""
    response_data = {"message": "Exception Raised", "details": str(exc)}
    return CustomJSONResponse(content=response_data, status_code=500)


register_tortoise(
    app=app,
    config=TORTOISE_CONFIG,
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.get("/news")
async def get_news(
    request: Request, page: int = Query(1, ge=1), limit: int = Query(10, ge=1)
):
    """Get news headlines with pagination."""
    pass


@app.post("/news/save-latest")
async def save_latest_news(request: Request):
    """Save the top three latest news headlines."""
    pass


@app.get("/news/headlines/country/{country_code}")
async def get_headlines_by_country(request: Request, country_code: str = Path(...)):
    """Get news headlines by country code."""
    pass


@app.get("/news/headlines/source/{source_id}")
async def get_headlines_by_source(request: Request, source_id: str = Path(...)):
    """Get news headlines by source ID."""
    pass


@app.get("/news/headlines/filter")
async def get_headlines_by_filter(
    request: Request, country: str = Query(None), source: str = Query(None)
):
    """Get news headlines by country or source."""
    pass
