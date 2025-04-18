import urllib.parse

from conf.paginations import Pagination
from conf.response import CustomJSONResponse
from utils.news_api_client import NewsAPI
from models import Article
from schemas import AllowedCountryCodes


async def get_news_view(search: str, page: int = 1, limit: int = 10):
    """View to get news headlines with pagination."""
    search = urllib.parse.quote(search)
    news_api_client = NewsAPI()
    news = await news_api_client.get_all_news(search=search, page=page, limit=limit)
    if news is None:
        return CustomJSONResponse(
            content=None, message="Failed to fetch the news", status_code=400
        )
    pagination = Pagination(
        page=page,
        limit=limit,
        total_count=news.get("totalResults"),
        data=news.get("articles"),
    )
    return CustomJSONResponse(content=pagination.get_paginated_data())


async def save_latest_news_view():
    """View to save the top three latest news headlines."""
    news_api_client = NewsAPI()
    top_three_articles = await news_api_client.get_top_three_headlines()
    if top_three_articles is None:
        return CustomJSONResponse(
            content=None,
            message="Failed to fetch the top three headlines",
            status_code=400,
        )
    saved_articles = []
    for article in top_three_articles:
        article_obj = await Article.create(
            **{
                "title": article.get("title"),
                "author": article.get("author"),
                "description": article.get("description"),
                "published_at": article.get("publishedAt"),
            }
        )
        saved_articles.append(article_obj.to_json())
    return CustomJSONResponse(
        content=saved_articles, message="Saved latest three headlines successfully"
    )


async def get_headlines_by_country_view(country_code: AllowedCountryCodes):
    """View to get news headlines by country code."""
    news_api_client = NewsAPI()
    articles = await news_api_client.get_headlines_by_country(country_code=country_code)
    if articles is None:
        return CustomJSONResponse(
            content=None,
            message="Failed to fetch the headlines",
            status_code=400,
        )
    return CustomJSONResponse(
        content=articles, message="Fetched headlines successfully"
    )


async def get_headlines_by_source_view(source_id: str):
    """View to get news headlines by source ID."""
    news_api_client = NewsAPI()
    articles = await news_api_client.get_headlines_by_source(source_id=source_id)
    if articles is None:
        return CustomJSONResponse(
            content=None,
            message="Failed to fetch the headlines",
            status_code=400,
        )
    return CustomJSONResponse(
        content=articles, message="Fetched headlines successfully"
    )


async def get_headlines_by_filter_view(
    country_code: AllowedCountryCodes = None, source_id: str = None
):
    """View to get news headlines by country, source or both."""
    if not country_code and not source_id:
        return CustomJSONResponse(
            content=None,
            message="country Or source Required",
            status_code=400,
        )
    news_api_client = NewsAPI()
    final_results = []
    if country_code and source_id:
        country_code_results = (
            await news_api_client.get_headlines_by_country(country_code=country_code)
            or []
        )
        for article in country_code_results:
            if article.get("source", {}).get("id") == source_id:
                final_results.append(article)
    elif country_code:
        final_results = await news_api_client.get_headlines_by_country(
            country_code=country_code
        )
    elif source_id:
        final_results = await news_api_client.get_headlines_by_source(
            source_id=source_id
        )
    if final_results is None:
        return CustomJSONResponse(
            content=None,
            message="Failed to fetch the headlines",
            status_code=400,
        )
    return CustomJSONResponse(
        content=final_results, message="Fetched headlines successfully"
    )
