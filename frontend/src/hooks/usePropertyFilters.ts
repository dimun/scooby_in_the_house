import { PropertySearchParams } from '../api/propertiesApi';
import { usePropertiesQuery } from './usePropertyQueries';
import { useForm } from './useForm';
import { useUrlParams } from './useUrlParams';

export const usePropertyFilters = () => {
  const { 
    getAllParams,
    getParam, 
    getNumberParam, 
    setParams, 
    clearParams 
  } = useUrlParams();
  
  // Initialize filter values from URL params
  const initialFilters: PropertySearchParams = {
    city: getParam('city', ''),
    region: getParam('region', ''),
    property_type: getParam('property_type', ''),
    min_price: getNumberParam('min_price'),
    max_price: getNumberParam('max_price'),
    min_rooms: getNumberParam('min_rooms'),
    min_bathrooms: getNumberParam('min_bathrooms'),
  };

  // Use the form hook to manage filter state
  const { values: filters, handleChange, reset } = useForm<PropertySearchParams>(initialFilters);

  // Get active filter count
  const activeFilterCount = Object.values(filters).filter(value => 
    value !== undefined && value !== ''
  ).length;

  // Use React Query to fetch properties
  const { 
    data: properties = [], 
    isLoading: loading, 
    error 
  } = usePropertiesQuery(getAllParams);

  const applyFilters = (e: React.FormEvent) => {
    e.preventDefault();
    setParams(filters as Record<string, string | number | boolean | undefined>);
  };

  const clearFilters = () => {
    reset({
      city: '',
      region: '',
      property_type: '',
      min_price: undefined,
      max_price: undefined,
      min_rooms: undefined,
      min_bathrooms: undefined,
    });
    clearParams();
  };

  return {
    properties,
    loading,
    error: error ? 'Failed to fetch properties' : '',
    filters,
    activeFilterCount,
    handleFilterChange: handleChange,
    applyFilters,
    clearFilters
  };
}; 