import pytest
from assertpy import assert_that
from sqlalchemy.orm import Session
from unittest.mock import create_autospec
from typing import Callable

from app.core.usecases.scraper_usecases import ScraperUseCases


@pytest.fixture
def mock_db():
    mock = create_autospec(Session)

    return mock


@pytest.fixture
def scraper_usecases(mock_db):
    return ScraperUseCases(db=mock_db)


@pytest.fixture
def mock_scrape_properties(monkeypatch):
    async def mock_async(city, region, property_type, max_pages, db, task_id):
        return task_id

    mock = create_autospec(mock_async, spec_set=True)
    mock.return_value = "test_task_id"
    monkeypatch.setattr("app.core.usecases.scraper_usecases.scrape_properties", mock)
    return mock


@pytest.mark.asyncio
async def test_start_scraper_should_return_task_id_and_message_when_scraping_job_starts(
    scraper_usecases: ScraperUseCases,
    mock_db: Session,
    mock_scrape_properties: Callable,
):
    # Arrange
    city = "Bogota"
    region = "Cundinamarca"
    property_types = ["apartamento", "casa"]
    max_pages = 2

    # Act
    result = await scraper_usecases.start_scraper(
        city=city, region=region, property_types=property_types, max_pages=max_pages
    )

    # Assert
    assert_that(result["task_id"]).is_length(12)
    assert_that(result["message"]).contains(
        "Scraping job started for apartamento-y-casa in Bogota, Cundinamarca"
    )


@pytest.mark.asyncio
async def test_start_scraper_should_call_scrape_properties_with_correct_parameters_when_scraping_job_starts(
    scraper_usecases: ScraperUseCases,
    mock_db: Session,
    mock_scrape_properties: Callable,
):
    # Arrange
    city = "Bogota"
    region = "Cundinamarca"
    property_types = ["apartamento", "casa"]
    max_pages = 2

    # Act
    await scraper_usecases.start_scraper(
        city=city, region=region, property_types=property_types, max_pages=max_pages
    )

    # Assert
    mock_scrape_properties.assert_called_once()
    call_args = mock_scrape_properties.call_args[1]
    assert_that(
        {
            "city": city,
            "region": region,
            "property_type": "apartamento-y-casa",
            "max_pages": max_pages,
            "db": mock_db,
        }
    ).is_subset_of(call_args)
