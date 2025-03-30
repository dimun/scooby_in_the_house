import React from 'react';
import { NavLink } from 'react-router-dom';

const NotFound: React.FC = () => {
  return (
    <div className="not-found">
      <h1>404 - Page Not Found</h1>
      <p>The page you are looking for does not exist.</p>
      <NavLink to="/" className="not-found-button">Go Home</NavLink>
    </div>
  );
};

export default NotFound; 