from fastapi import APIRouter, Request, Path, Query, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer

from conf.permissions import IsAuthenticated
from views import (
    get_news_view,
    save_latest_news_view,
    get_headlines_by_country_view,
    get_headlines_by_source_view,
    get_headlines_by_filter_view,
)
from schemas import AllowedCountryCodes


oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl="code", tokenUrl="token")
router = APIRouter(
    prefix="/news",
    tags=["news"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme), Depends(IsAuthenticated())],
)


@router.get("")
async def get_news(
    _request: Request,
    search: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
):
    """Get news headlines with pagination."""
    return await get_news_view(search=search, page=page, limit=limit)


@router.post("/save-latest")
async def save_latest_news(_request: Request):
    """Save the top three latest news headlines."""
    return await save_latest_news_view()


@router.get("/headlines/country/{country_code}")
async def get_headlines_by_country(_request: Request, country_code: AllowedCountryCodes = Path(...)):
    """Get news headlines by country code."""
    return await get_headlines_by_country_view(country_code=country_code)


@router.get("/headlines/source/{source_id}")
async def get_headlines_by_source(_request: Request, source_id: str = Path(...)):
    """Get news headlines by source ID."""
    return await get_headlines_by_source_view(source_id=source_id)


@router.get("/headlines/filter")
async def get_headlines_by_filter(
    _request: Request, country: AllowedCountryCodes = Query(None), source: str = Query(None)
):
    """Get news headlines by country or source."""
    return await get_headlines_by_filter_view(country_code=country, source_id=source)
