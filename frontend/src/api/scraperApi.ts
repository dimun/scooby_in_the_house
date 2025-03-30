import apiClient from './client';

// Define types for scraper data
export interface ScraperParams {
  city: string;
  region: string;
  property_types: string[];
  max_pages: number;
}

export interface ScraperResponse {
  message: string;
  task_id?: string;
  status?: string;
}

export interface ScraperLogsResponse {
  logs: string[];
}

export interface TaskStatus {
  id: string;
  city: string;
  region: string;
  property_type: string;
  max_pages: number;
  status: string;
  properties_found?: number;
  error?: string;
  start_time: string;
  end_time?: string;
  duration_seconds?: number;
}

export interface TaskListResponse {
  tasks: TaskStatus[];
  total: number;
}

// API functions
export const startScraper = async (params: ScraperParams): Promise<ScraperResponse> => {
  const response = await apiClient.post('/api/v1/scrape', {
    city: params.city.toLowerCase(),
    region: params.region.toLowerCase(),
    property_types: params.property_types,
    max_pages: params.max_pages,
  });
  return response.data;
};

export const getScraperStatus = async (taskId?: string): Promise<TaskListResponse> => {
  const url = taskId ? `/api/v1/scrape/status?task_id=${taskId}` : '/api/v1/scrape/status';
  const response = await apiClient.get(url);
  return response.data;
};

export const getScraperLogs = async (taskId?: string, limit: number = 20): Promise<ScraperLogsResponse> => {
  const url = taskId 
    ? `/api/v1/scrape/logs?task_id=${taskId}&limit=${limit}` 
    : `/api/v1/scrape/logs?limit=${limit}`;
  const response = await apiClient.get(url);
  return response.data;
};

// Export all functions as a default object for convenience
const scraperApi = {
  startScraper,
  getScraperStatus,
  getScraperLogs
};

export default scraperApi; 