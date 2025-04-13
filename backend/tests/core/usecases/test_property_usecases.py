import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from typing import List
from assertpy import assert_that
from app.core.usecases.property_usecases import PropertyUseCases
from app.models.property import Property

@pytest.fixture
def mock_db():
    return Mock(spec=Session)

def test_get_properties_should_return_filtered_properties_when_filters_are_provided(mock_db: Session):
    # Arrange
    mock_property_repo = Mock()
    mock_property_repo.get_properties_with_filters.return_value = [
        Property(id=1, city="Madrid", region="Centro", price=300000),
        Property(id=2, city="Madrid", region="Centro", price=350000)
    ]
    
    with patch('app.core.usecases.property_usecases.PropertyRepository', return_value=mock_property_repo):
        usecase = PropertyUseCases(mock_db)
        
        # Act
        result = usecase.get_properties(
            city="Madrid",
            region="Centro",
            min_price=300000,
            max_price=400000
        )
        
        # Assert
        assert_that(result).is_length(2)
        mock_property_repo.get_properties_with_filters.assert_called_once_with(
            city="Madrid",
            region="Centro",
            property_type=None,
            min_price=300000,
            max_price=400000,
            min_rooms=None,
            min_bathrooms=None,
            skip=0,
            limit=20
        )

def test_get_properties_should_return_all_properties_when_no_filters_are_provided(mock_db: Session):
    # Arrange
    mock_property_repo = Mock()
    mock_property_repo.get_properties_with_filters.return_value = [
        Property(id=1, city="Madrid", region="Centro", price=300000),
        Property(id=2, city="Barcelona", region="Eixample", price=400000)
    ]
    
    with patch('app.core.usecases.property_usecases.PropertyRepository', return_value=mock_property_repo):
        usecase = PropertyUseCases(mock_db)
        
        # Act
        result = usecase.get_properties()
        
        # Assert
        assert_that(result).is_length(2)
        mock_property_repo.get_properties_with_filters.assert_called_once_with(
            city=None,
            region=None,
            property_type=None,
            min_price=None,
            max_price=None,
            min_rooms=None,
            min_bathrooms=None,
            skip=0,
            limit=20
        )

def test_get_property_stats_should_return_correct_statistics(mock_db: Session):
    # Arrange
    mock_property_repo = Mock()
    mock_property_repo.get_property_count.return_value = 100
    mock_property_repo.get_property_count_by_city.return_value = {
        "Madrid": 50,
        "Barcelona": 30,
        "Valencia": 20
    }
    mock_property_repo.get_avg_price_by_city.return_value = {
        "Madrid": 300000,
        "Barcelona": 400000,
        "Valencia": 200000
    }
    
    with patch('app.core.usecases.property_usecases.PropertyRepository', return_value=mock_property_repo):
        usecase = PropertyUseCases(mock_db)
        
        # Act
        result = usecase.get_property_stats()
        
        # Assert
        assert_that(result["total_properties"]).is_equal_to(100)
        assert_that(result["by_city"]).is_equal_to({
            "Madrid": 50,
            "Barcelona": 30,
            "Valencia": 20
        })
        assert_that(result["avg_prices"]).is_equal_to({
            "Madrid": 300000,
            "Barcelona": 400000,
            "Valencia": 200000
        })
        mock_property_repo.get_property_count.assert_called_once()
        mock_property_repo.get_property_count_by_city.assert_called_once()
        mock_property_repo.get_avg_price_by_city.assert_called_once() 