import React from 'react';
import { PropertySearchParams } from '../../api/propertiesApi';
import { useFilterUI } from '../../hooks';
import './PropertyFilter.css';

interface PropertyFilterProps {
  filters: PropertySearchParams;
  onFilterChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onFilterApply: (e: React.FormEvent) => void;
  onFilterClear: () => void;
}

const PropertyFilter: React.FC<PropertyFilterProps> = ({
  filters,
  onFilterChange,
  onFilterApply,
  onFilterClear
}) => {
  const { isExpanded, toggleFilters, hasActiveFilters } = useFilterUI(filters);

  return (
    <div className="filter-container">
      {/* Filter header with toggle */}
      <div className="filter-header" onClick={toggleFilters}>
        <div className="filter-title">
          <h2>Filter Properties</h2>
          {hasActiveFilters && (
            <span className="filter-badge">Active</span>
          )}
        </div>
        <svg 
          className={`filter-toggle-icon ${isExpanded ? 'active' : ''}`} 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </div>
      
      {/* Filter form */}
      {isExpanded && (
        <form onSubmit={onFilterApply} className="filter-form">
          {/* City and Region row */}
          <div className="filter-row">
            <div className="filter-field">
              <label className="filter-label" htmlFor="city">City</label>
              <input
                className="filter-input"
                type="text"
                id="city"
                name="city"
                value={filters.city || ''}
                onChange={onFilterChange}
                placeholder="e.g., manizales"
              />
            </div>
            
            <div className="filter-field">
              <label className="filter-label" htmlFor="region">Region</label>
              <input
                className="filter-input"
                type="text"
                id="region"
                name="region"
                value={filters.region || ''}
                onChange={onFilterChange}
                placeholder="e.g., caldas"
              />
            </div>
          </div>
          
          {/* Property Type row */}
          <div className="filter-row">
            <div className="filter-field-full">
              <label className="filter-label" htmlFor="property_type">Property Type</label>
              <input
                className="filter-input"
                type="text"
                id="property_type"
                name="property_type"
                value={filters.property_type || ''}
                onChange={onFilterChange}
                placeholder="e.g., Apartamento"
              />
            </div>
          </div>
          
          {/* Price range row */}
          <div className="filter-row">
            <div className="filter-field">
              <label className="filter-label" htmlFor="min_price">Min Price</label>
              <input
                className="filter-input"
                type="number"
                id="min_price"
                name="min_price"
                value={filters.min_price || ''}
                onChange={onFilterChange}
                placeholder="Minimum price"
              />
            </div>
            
            <div className="filter-field">
              <label className="filter-label" htmlFor="max_price">Max Price</label>
              <input
                className="filter-input"
                type="number"
                id="max_price"
                name="max_price"
                value={filters.max_price || ''}
                onChange={onFilterChange}
                placeholder="Maximum price"
              />
            </div>
          </div>
          
          {/* Rooms and Bathrooms row */}
          <div className="filter-row">
            <div className="filter-field">
              <label className="filter-label" htmlFor="min_rooms">Min Rooms</label>
              <input
                className="filter-input"
                type="number"
                id="min_rooms"
                name="min_rooms"
                value={filters.min_rooms || ''}
                onChange={onFilterChange}
                placeholder="Minimum rooms"
                min="1"
              />
            </div>
            
            <div className="filter-field">
              <label className="filter-label" htmlFor="min_bathrooms">Min Bathrooms</label>
              <input
                className="filter-input"
                type="number"
                id="min_bathrooms"
                name="min_bathrooms"
                value={filters.min_bathrooms || ''}
                onChange={onFilterChange}
                placeholder="Minimum bathrooms"
                min="1"
              />
            </div>
          </div>
          
          {/* Action buttons */}
          <div className="filter-actions">
            <button type="submit" className="filter-button filter-button-apply">
              Apply Filters
            </button>
            <button 
              type="button" 
              className="filter-button filter-button-clear"
              onClick={onFilterClear}
            >
              Clear Filters
            </button>
            <button 
              type="button" 
              className="filter-button filter-button-close"
              onClick={toggleFilters}
            >
              Close Filters
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default PropertyFilter; 