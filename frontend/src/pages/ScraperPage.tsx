import React from 'react';
import PropertyScraper from '../components/PropertyScraper';

const ScraperPage: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold mb-6">Property Scraper</h1>
      <PropertyScraper />
    </div>
  );
};

export default ScraperPage; 