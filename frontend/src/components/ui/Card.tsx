import React from 'react';

interface CardProps {
  title?: string;
  children: React.ReactNode;
  className?: string;
  bodyClassName?: string;
  variant?: 'light' | 'dark';
}

const Card: React.FC<CardProps> = ({
  title,
  children,
  className = '',
  bodyClassName = '',
  variant = 'light'
}) => {
  const baseClasses = 'rounded-lg shadow overflow-hidden';
  const variantClasses = variant === 'dark' ? 'bg-gray-900 text-white' : 'bg-white text-gray-900';
  
  return (
    <div className={`${baseClasses} ${variantClasses} ${className}`}>
      {title && (
        <div className={`border-b ${variant === 'dark' ? 'border-gray-800' : 'border-gray-200'} px-4 py-3`}>
          <h3 className={`text-lg font-medium ${variant === 'dark' ? 'text-white' : 'text-gray-900'}`}>{title}</h3>
        </div>
      )}
      <div className={`${bodyClassName}`}>
        {children}
      </div>
    </div>
  );
};

export default Card; 