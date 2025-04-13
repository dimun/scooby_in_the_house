import React from 'react';
import './PropertyCard.css';

interface PropertyActionButtonProps {
  url?: string;
}

const PropertyActionButton: React.FC<PropertyActionButtonProps> = ({ url }) => {
  return (
    <div className="property-action">
      {url ? (
        <a 
          href={url}
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
  );
};

export default PropertyActionButton; 