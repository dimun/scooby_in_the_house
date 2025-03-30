import { useQuery } from '@tanstack/react-query';
import propertiesApi, { Property } from '../api/propertiesApi';

export const usePropertiesQuery = (params: Record<string, string>) => {
  return useQuery({
    queryKey: ['properties', params],
    queryFn: () => propertiesApi.getProperties(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
    placeholderData: (previousData) => previousData, // Use previous data while loading
  });
};

// Hook for getting property stats by city
export const usePropertyStatsByCityQuery = () => {
  return useQuery({
    queryKey: ['propertyStatsByCity'],
    queryFn: () => propertiesApi.getPropertyStatsByCity(),
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
};

// Hook for getting property average prices
export const usePropertyAvgPricesQuery = () => {
  return useQuery({
    queryKey: ['propertyAvgPrices'],
    queryFn: () => propertiesApi.getPropertyAvgPrices(),
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
}; 