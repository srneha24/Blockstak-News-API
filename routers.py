from fastapi import APIRouter, Request, Path, Query

from views import (
    get_news_view,
    save_latest_news_view,
    get_headlines_by_country_view,
    get_headlines_by_source_view,
    get_headlines_by_filter_view
)


router = APIRouter(prefix="", responses={404: {"description": "Not found"}})


@router.get("/news")
async def get_news(
    request: Request, page: int = Query(1, ge=1), limit: int = Query(10, ge=1)
):
    """Get news headlines with pagination."""
    return await get_news_view(page=page, limit=limit)


@router.post("/news/save-latest")
async def save_latest_news(request: Request):
    """Save the top three latest news headlines."""
    return await save_latest_news_view()


@router.get("/news/headlines/country/{country_code}")
async def get_headlines_by_country(request: Request, country_code: str = Path(...)):
    """Get news headlines by country code."""
    return await get_headlines_by_country_view(country_code=country_code)


@router.get("/news/headlines/source/{source_id}")
async def get_headlines_by_source(request: Request, source_id: str = Path(...)):
    """Get news headlines by source ID."""
    return await get_headlines_by_source_view(source_id=source_id)


@router.get("/news/headlines/filter")
async def get_headlines_by_filter(
    request: Request, country: str = Query(None), source: str = Query(None)
):
    """Get news headlines by country or source."""
    return await get_headlines_by_filter_view(country_code=country, source_id=source)
