import { PropertyFilter, PropertyList } from '../components';
import { usePropertyFilters } from '../hooks';
import './PropertiesPage.css';

const PropertiesPage = () => {
  const {
    properties,
    loading,
    error,
    filters,
    activeFilterCount,
    handleFilterChange,
    applyFilters,
    clearFilters
  } = usePropertyFilters();

  return (
    <div className="properties-page">
      <div className="properties-container">
        <div className="properties-header">
          <h1 className="properties-title">Real Estate Properties</h1>
          
          {!loading && properties.length > 0 && (
            <div className="properties-count">
              Showing {properties.length} {properties.length === 1 ? 'property' : 'properties'}
              {activeFilterCount > 0 && <span> with {activeFilterCount} active {activeFilterCount === 1 ? 'filter' : 'filters'}</span>}
            </div>
          )}
        </div>
        
        <PropertyFilter 
          filters={filters}
          onFilterChange={handleFilterChange}
          onFilterApply={applyFilters}
          onFilterClear={clearFilters}
        />
        
        <PropertyList 
          properties={properties}
          loading={loading}
          error={error}
        />
      </div>
    </div>
  );
};

export default PropertiesPage; 