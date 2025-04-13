import React, { useState } from 'react';
import { Property } from '../../api/propertiesApi';
import './PropertyCard.css'; // We'll create this file next

interface PropertyCardProps {
  property: Property;
}

const PropertyCard: React.FC<PropertyCardProps> = ({ property }) => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  const formatPrice = (price: number | null) => {
    if (price === null) return 'Price not available';
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(price);
  };

  const handlePrevImage = () => {
    if (property.image_urls && property.image_urls.length > 0) {
      setCurrentImageIndex((prev) => 
        prev === 0 ? property.image_urls!.length - 1 : prev - 1
      );
    }
  };

  const handleNextImage = () => {
    if (property.image_urls && property.image_urls.length > 0) {
      setCurrentImageIndex((prev) => 
        prev === property.image_urls!.length - 1 ? 0 : prev + 1
      );
    }
  };

  return (
    <div className="property-card">
      {/* Image Carousel */}
      {property.image_urls && property.image_urls.length > 0 ? (
        <div className="property-image-container">
          <img 
            src={property.image_urls[currentImageIndex]} 
            alt={property.title || 'Property image'} 
            className="property-image"
          />
          {property.image_urls.length > 1 && (
            <>
              <button 
                className="image-nav-button prev" 
                onClick={handlePrevImage}
                aria-label="Previous image"
              >
                &lt;
              </button>
              <button 
                className="image-nav-button next" 
                onClick={handleNextImage}
                aria-label="Next image"
              >
                &gt;
              </button>
              <div className="image-counter">
                {currentImageIndex + 1} / {property.image_urls.length}
              </div>
            </>
          )}
        </div>
      ) : (
        <div className="property-image-placeholder">
          No images available
        </div>
      )}

      <div className="property-content">
        {/* Header with title and price */}
        <div className="property-header">
          <h3 className="property-title">{property.title || 'Unnamed Property'}</h3>
          <div className="property-price">
            {formatPrice(property.price)}
          </div>
        </div>
        
        {/* Property details */}
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
        
        {/* Location */}
        <div className="property-location">
          {property.city && property.region && (
            <div className="location-text">
              {property.city}, {property.region}
            </div>
          )}
        </div>
      </div>
      
      {/* Red action button at bottom */}
      <div className="property-action">
        {property.url ? (
          <a 
            href={property.url}
            target="_blank"
            rel="noopener noreferrer"
            className="view-listing-button"
          >
            View Original Listing
          </a>
        ) : (
          <div className="empty-button"></div>
        )}
      </div>
    </div>
  );
};

export default PropertyCard; 