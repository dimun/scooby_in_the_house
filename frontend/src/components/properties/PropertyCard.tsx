import React from 'react';
import { Property } from '../../api/propertiesApi';
import PropertyImageCarousel from './PropertyImageCarousel';
import PropertyDetails from './PropertyDetails';
import PropertyActionButton from './PropertyActionButton';
import './PropertyCard.css'; // We'll create this file next

interface PropertyCardProps {
  property: Property;
}

const PropertyCard: React.FC<PropertyCardProps> = ({ property }) => {
  return (
    <div className="property-card">
      <PropertyImageCarousel 
        imageUrls={property.image_urls} 
        title={property.title}
      />
      <PropertyDetails property={property} />
      <PropertyActionButton url={property.url} />
    </div>
  );
};

export default PropertyCard; 