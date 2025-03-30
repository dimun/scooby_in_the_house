import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface SearchFormData {
  city: string;
  region: string;
  property_type: string;
  min_price: string;
  max_price: string;
  min_rooms: string;
  min_bathrooms: string;
}

const SearchPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<SearchFormData>({
    city: '',
    region: '',
    property_type: '',
    min_price: '',
    max_price: '',
    min_rooms: '',
    min_bathrooms: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Build query parameters for the properties page
    const params = new URLSearchParams();
    
    // Add non-empty parameters
    Object.entries(formData).forEach(([key, value]) => {
      if (value) {
        params.append(key, value);
      }
    });

    // Navigate to properties page with search parameters
    navigate(`/properties?${params.toString()}`);
  };

  return (
    <div className="container">
      <header className="header">
        <h1>Scooby In The House</h1>
        <nav>
          <a href="/">Home</a>
          <a href="/properties">Properties</a>
          <a href="/scraper">Scraper</a>
          <a href="/search" className="active">Search</a>
        </nav>
      </header>
      
      <main>
        <div className="search-page">
          <h1>Advanced Property Search</h1>
          <p>Search for your ideal property with specific criteria</p>
          
          <form onSubmit={handleSubmit} className="search-form">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="city">City</label>
                <input
                  type="text"
                  id="city"
                  name="city"
                  value={formData.city}
                  onChange={handleChange}
                  placeholder="e.g., manizales"
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="region">Region</label>
                <input
                  type="text"
                  id="region"
                  name="region"
                  value={formData.region}
                  onChange={handleChange}
                  placeholder="e.g., caldas"
                />
              </div>
            </div>
            
            <div className="form-group">
              <label htmlFor="property_type">Property Type</label>
              <select
                id="property_type"
                name="property_type"
                value={formData.property_type}
                onChange={handleChange}
              >
                <option value="">All Types</option>
                <option value="Apartamento">Apartment</option>
                <option value="Casa">House</option>
                <option value="Lote">Land</option>
              </select>
            </div>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="min_price">Min Price</label>
                <input
                  type="number"
                  id="min_price"
                  name="min_price"
                  value={formData.min_price}
                  onChange={handleChange}
                  placeholder="Minimum price"
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="max_price">Max Price</label>
                <input
                  type="number"
                  id="max_price"
                  name="max_price"
                  value={formData.max_price}
                  onChange={handleChange}
                  placeholder="Maximum price"
                />
              </div>
            </div>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="min_rooms">Min Rooms</label>
                <input
                  type="number"
                  id="min_rooms"
                  name="min_rooms"
                  value={formData.min_rooms}
                  onChange={handleChange}
                  placeholder="Minimum rooms"
                  min="1"
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="min_bathrooms">Min Bathrooms</label>
                <input
                  type="number"
                  id="min_bathrooms"
                  name="min_bathrooms"
                  value={formData.min_bathrooms}
                  onChange={handleChange}
                  placeholder="Minimum bathrooms"
                  min="1"
                />
              </div>
            </div>
            
            <button type="submit" className="search-button">Search Properties</button>
          </form>
          
          <div className="search-info">
            <h3>Search Tips</h3>
            <ul>
              <li>Leave fields blank to see all available properties</li>
              <li>Specify both city and region for more accurate results</li>
              <li>Use min/max price to find properties within your budget</li>
              <li>Minimum rooms and bathrooms help filter for family-sized properties</li>
            </ul>
          </div>
        </div>
      </main>
      
      <footer>
        <p>&copy; {new Date().getFullYear()} Scooby In The House. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default SearchPage; 