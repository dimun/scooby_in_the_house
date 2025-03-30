import { useState } from 'react';
import { PropertySearchParams } from '../api/propertiesApi';

export const useFilterUI = (filters: PropertySearchParams) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleFilters = () => {
    setIsExpanded(!isExpanded);
  };

  const hasActiveFilters = Object.values(filters).some(value => 
    value !== undefined && value !== ''
  );

  return {
    isExpanded,
    toggleFilters,
    hasActiveFilters
  };
}; 