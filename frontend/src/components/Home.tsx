import React from 'react';
import { NavLink } from 'react-router-dom';

const Home: React.FC = () => {
  return (
    <div className="home-container">
      <div className="hero-section">
        <div className="hero-logo">
          <img src="/dark_theme_logo_inverted.png" alt="Scooby In The House" className="hero-logo-image" />
        </div>
        <h1>Find Your Dream Property in Colombia</h1>
        <p>Browse our extensive collection of houses, apartments, and more</p>
        <div className="hero-actions">
          <NavLink to="/properties" className="hero-button">View Properties</NavLink>
          <NavLink to="/scraper" className="hero-button secondary">Scrape Properties</NavLink>
        </div>
      </div>
    </div>
  );
};

export default Home; 