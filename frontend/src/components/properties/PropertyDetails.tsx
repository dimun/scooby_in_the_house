import React from 'react';
import { Property } from '../../api/propertiesApi';
import './PropertyCard.css';

interface PropertyDetailsProps {
  property: Property;
}

const PropertyDetails: React.FC<PropertyDetailsProps> = ({ property }) => {
  const formatPrice = (price: number | null) => {
    if (price === null) return 'Price not available';
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(price);
  };

  return (
    <div className="property-content">
      <div className="property-header">
        <h3 className="property-title">{property.title || 'Unnamed Property'}</h3>
        <div className="property-price">
          {formatPrice(property.price)}
        </div>
      </div>
      
      <div className="property-details">
        <div className="property-specs">
          {property.rooms && (
            <div className="property-spec">
              {property.rooms} Rooms
            </div>
          )}
          
          {property.bathrooms && (
            <div className="property-spec">
              {property.bathrooms} Baths
            </div>
          )}
          
          {property.surface && (
            <div className="property-spec">
              {property.surface} {property.surface_unit || 'm²'}
            </div>
          )}
          
          {property.property_type && (
            <div className="property-spec">
              <span className="property-type">{property.property_type}</span>
            </div>
          )}
        </div>
      </div>
      
      <div className="property-location">
        {property.city && property.region && (
          <div className="location-text">
            {property.city}, {property.region}
          </div>
        )}
      </div>
    </div>
  );
};

export default PropertyDetails; 