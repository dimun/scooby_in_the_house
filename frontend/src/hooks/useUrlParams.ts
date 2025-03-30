import { useSearchParams } from 'react-router-dom';
import { useMemo } from 'react';

/**
 * A hook for handling URL search parameters
 * @returns Methods for working with URL search parameters
 */
export const useUrlParams = () => {
  const [searchParams, setSearchParams] = useSearchParams();

  // Get a typed parameter from the URL
  const getParam = <T>(
    key: string, 
    defaultValue: T, 
    parser?: (value: string) => T
  ): T => {
    const value = searchParams.get(key);
    if (value === null) return defaultValue;
    if (parser) return parser(value);
    return value as unknown as T;
  };

  // Get a number parameter
  const getNumberParam = (key: string, defaultValue?: number): number | undefined => {
    const value = searchParams.get(key);
    if (value === null) return defaultValue;
    const parsed = Number(value);
    return isNaN(parsed) ? defaultValue : parsed;
  };

  // Get all parameters as an object
  const getAllParams = useMemo(() => {
    const params: Record<string, string> = {};
    for (const [key, value] of searchParams.entries()) {
      params[key] = value;
    }
    return params;
  }, [searchParams]);

  // Set multiple parameters at once
  const setParams = (params: Record<string, string | number | boolean | undefined>): void => {
    const newParams = new URLSearchParams();
    
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== '') {
        newParams.set(key, String(value));
      }
    });
    
    setSearchParams(newParams);
  };

  // Clear all parameters
  const clearParams = (): void => {
    setSearchParams(new URLSearchParams());
  };

  return {
    searchParams,
    setSearchParams,
    getParam,
    getNumberParam,
    getAllParams,
    setParams,
    clearParams
  };
}; 