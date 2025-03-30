import React from 'react';
import { Property } from '../../api/propertiesApi';
import PropertyCard from './PropertyCard';
import './PropertyList.css';

interface PropertyListProps {
  properties: Property[];
  loading: boolean;
  error: string;
}

const PropertyList: React.FC<PropertyListProps> = ({ properties, loading, error }) => {
  if (loading) {
    return (
      <div className="loading">
        <div className="loading-spinner"></div>
        <p className="loading-text">Loading properties...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-message">
        <div className="error-title">Error</div>
        <p>{error}</p>
      </div>
    );
  }

  if (properties.length === 0) {
    return (
      <div className="no-results">
        <svg className="no-results-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 className="no-results-title">No properties found</h3>
        <p className="no-results-message">
          Try adjusting your filters or scrape new data to find properties that match your criteria.
        </p>
      </div>
    );
  }

  return (
    <div className="property-list">
      <div className="properties-grid">
        {properties.map((property) => (
          <PropertyCard key={property.id} property={property} />
        ))}
      </div>
    </div>
  );
};

export default PropertyList; 