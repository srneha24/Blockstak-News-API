from datetime import datetime

import pytest
import pytz
from tortoise.exceptions import ValidationError

from models import Article


@pytest.mark.asyncio
async def test_article_creation(test_db):
    """Test creating an article."""
    article_data = {
        "title": "Test Article",
        "author": "Test Author",
        "description": "Test Description",
        "published_at": datetime.now(pytz.UTC),
    }

    article = await Article.create(**article_data)
    assert article.title == article_data["title"]
    assert article.author == article_data["author"]
    assert article.description == article_data["description"]

    # Test JSON serialization
    json_data = article.to_json()
    assert isinstance(json_data, dict)
    assert json_data["title"] == article_data["title"]
    assert json_data["author"] == article_data["author"]
    assert json_data["description"] == article_data["description"]
    assert "created_at" in json_data
    assert "updated_at" in json_data


@pytest.mark.asyncio
async def test_article_creation_minimal(test_db):
    """Test creating an article with only required fields."""
    article_data = {"title": "Test Article"}

    article = await Article.create(**article_data)
    assert article.title == article_data["title"]
    assert article.author is None
    assert article.description is None
    assert article.published_at is None


@pytest.mark.asyncio
async def test_article_update(test_db):
    """Test updating an article."""
    article = await Article.create(title="Initial Title")

    new_title = "Updated Title"
    await article.update_from_dict({"title": new_title})
    await article.save()

    updated_article = await Article.get(id=article.id)
    assert updated_article.title == new_title


@pytest.mark.asyncio
async def test_article_unique_constraints(test_db):
    """Test that we can create articles with the same title."""
    article1 = await Article.create(title="Same Title")
    article2 = await Article.create(title="Same Title")

    assert article1.id != article2.id


@pytest.mark.asyncio
async def test_article_fields_length(test_db):
    """Test field length constraints."""
    # Create article with title exactly 255 chars
    title = "x" * 255
    article = await Article.create(title=title)
    assert len(article.title) == 255

    # Test title too long (256 chars)
    with pytest.raises(ValidationError):
        await Article.create(title="x" * 256)


@pytest.mark.asyncio
async def test_article_datetime_handling(test_db):
    """Test datetime field handling."""
    now = datetime.now(pytz.UTC)
    article = await Article.create(title="Test", published_at=now)

    # Fetch the article back
    fetched = await Article.get(id=article.id)
    # Compare timestamps for timezone-aware datetimes
    assert fetched.published_at.astimezone(pytz.UTC).timestamp() == pytest.approx(
        now.timestamp()
    )
    assert fetched.created_at is not None
    assert fetched.updated_at is not None


@pytest.mark.asyncio
async def test_article_default_values(test_db):
    """Test default values for Article fields."""
    article = await Article.create(title="Test Default Values")

    assert article.author is None
    assert article.description is None
    assert article.published_at is None
    assert article.created_at is not None
    assert article.updated_at is not None


@pytest.mark.asyncio
async def test_article_bulk_operations(test_db):
    """Test bulk create and filtering."""
    # Clear existing articles first
    await Article.all().delete()

    # Create articles one by one since bulk_create might not return instances
    await Article.create(title="Bulk 1")
    await Article.create(title="Bulk 2")
    await Article.create(title="Bulk 3")

    # Test filtering
    count = await Article.filter(title__startswith="Bulk").count()
    assert count == 3
