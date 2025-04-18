from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException

from conf.vars import NEWS_API_KEY
from utils.log import Log


class NewsAPI:
    """A client class for interacting with the News API."""

    client: NewsApiClient

    def __init__(self):
        self.client = NewsApiClient(api_key=NEWS_API_KEY)

    async def get_all_news(self, search: str, page: int, limit: int):
        """Get all news articles based on search query with pagination."""
        try:
            news = self.client.get_everything(q=search, page=page, page_size=limit)
            return news
        except NewsAPIException as e:
            Log.error(
                message="Failed: Encountered NewsAPIException", data={"error": str(e)}
            )
            return None

    async def get_top_three_headlines(self):
        """Get the top three headlines in the US."""
        try:
            top_three_headlines = self.client.get_top_headlines(
                country="us", page_size=5, page=1
            )
            articles = top_three_headlines.get("articles")
            return articles[:3] if articles else []
        except NewsAPIException as e:
            Log.error(
                message="Failed: Encountered NewsAPIException", data={"error": str(e)}
            )
            return None

    async def get_headlines_by_country(self, country_code: str):
        """Get news headlines by country code."""
        try:
            headlines = self.client.get_top_headlines(country=country_code)
            articles = headlines.get("articles")
            return articles
        except NewsAPIException as e:
            Log.error(
                message="Failed: Encountered NewsAPIException", data={"error": str(e)}
            )
            return None

    async def get_headlines_by_source(self, source_id: str):
        """Get news headlines by source ID."""
        source_id = "-".join(
            source_id.lower().split()
        )  # Converting to News API source ID format
        try:
            headlines = self.client.get_top_headlines(sources=source_id)
            articles = headlines.get("articles")
            return articles
        except NewsAPIException as e:
            Log.error(
                message="Failed: Encountered NewsAPIException", data={"error": str(e)}
            )
            return None
