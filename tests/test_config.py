from datetime import datetime, timedelta

# Test database configuration
TEST_DB_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {"file_path": ":memory:"}
        }
    },
    "apps": {
        "models": {
            "models": ["models"],
            "default_connection": "default"
        }
    },
    "use_tz": True
}

# Mock data for tests
MOCK_ARTICLE = {
    "title": "Test Article",
    "author": "Test Author",
    "description": "Test Description",
    "published_at": datetime.now()
}

MOCK_NEWS_RESPONSE = {
    "status": "ok",
    "totalResults": 10033,
    "articles": [
        {
            "source": {"id": "bbc-news", "name": "BBC News"},
            "author": "BBC News",
            "title": "Test Article 1",
            "description": "Test Description 1",
            "url": "https://www.bbc.com/news/test1",
            "urlToImage": "https://test.com/image1.jpg",
            "publishedAt": (datetime.now() - timedelta(days=1)).isoformat(),
            "content": "Test content 1"
        },
        {
            "source": {"id": "cnn", "name": "CNN"},
            "author": "CNN News",
            "title": "Test Article 2",
            "description": "Test Description 2",
            "url": "https://www.cnn.com/news/test2",
            "urlToImage": "https://test.com/image2.jpg",
            "publishedAt": datetime.now().isoformat(),
            "content": "Test content 2"
        }
    ]
}

# Test client credentials
TEST_CLIENT_ID = "demo-client"
TEST_CLIENT_SECRET = "C51D80D50A15DF7D"

# Test auth tokens
TEST_VALID_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vLWNsaWVudCIsImV4cCI6MTc0NDk4NTc3OC41MzE2M30.V-_Bkux53_6owIYxLUBTI5Spz8ev4a-Yb0RcdoyiQ0k"
TEST_EXPIRED_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vLWNsaWVudCIsImV4cCI6MTY0NDk4NTc3OC41MzE2M30.vF_yqo4SRA7dpjkJc3LL6VAqxUxkPdRYwKbwZxvqxbk"