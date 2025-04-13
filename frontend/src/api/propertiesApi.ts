import apiClient from './client';

// Define types for property data
export interface Property {
  id: number;
  url: string;
  title: string | null;
  price: number | null;
  rooms: number | null;
  bathrooms: number | null;
  surface: number | null;
  surface_unit: string | null;
  city: string | null;
  region: string | null;
  property_type: string | null;
  image_urls: string[] | null;
  created_at: string;
  updated_at: string | null;
}

// Define property filter parameters interface
export interface PropertySearchParams {
  city?: string;
  region?: string;
  property_type?: string;
  min_price?: number;
  max_price?: number;
  min_rooms?: number;
  min_bathrooms?: number;
  skip?: number;
  limit?: number;
}

// API functions
export const getProperties = async (params: PropertySearchParams = {}): Promise<Property[]> => {
  const response = await apiClient.get('/api/v1/properties', { params });
  return response.data;
};

export const getPropertyStatsByCity = async (): Promise<{city: string, count: number}[]> => {
  const response = await apiClient.get('/api/v1/properties/stats/city');
  return response.data;
};

export const getPropertyAvgPrices = async (): Promise<{city: string, avg_price: number}[]> => {
  const response = await apiClient.get('/api/v1/properties/stats/price');
  return response.data;
};

// Export all functions as a default object for convenience
const propertiesApi = {
  getProperties,
  getPropertyStatsByCity,
  getPropertyAvgPrices
};

export default propertiesApi; 