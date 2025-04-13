import React, { useState } from 'react';
import './PropertyCard.css';

interface PropertyImageCarouselProps {
  imageUrls: string[] | null;
  title?: string | null;
}

const PropertyImageCarousel: React.FC<PropertyImageCarouselProps> = ({ imageUrls, title }) => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  const handlePrevImage = () => {
    if (imageUrls && imageUrls.length > 0) {
      setCurrentImageIndex((prev) => 
        prev === 0 ? imageUrls.length - 1 : prev - 1
      );
    }
  };

  const handleNextImage = () => {
    if (imageUrls && imageUrls.length > 0) {
      setCurrentImageIndex((prev) => 
        prev === imageUrls.length - 1 ? 0 : prev + 1
      );
    }
  };

  if (!imageUrls || imageUrls.length === 0) {
    return (
      <div className="property-image-placeholder">
        No images available
      </div>
    );
  }

  return (
    <div className="property-image-container">
      <img 
        src={imageUrls[currentImageIndex]} 
        alt={title || 'Property image'} 
        className="property-image"
      />
      {imageUrls.length > 1 && (
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
            {currentImageIndex + 1} / {imageUrls.length}
          </div>
        </>
      )}
    </div>
  );
};

export default PropertyImageCarousel; 