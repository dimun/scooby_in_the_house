import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helpText?: string;
  fullWidth?: boolean;
}

const Input: React.FC<InputProps> = ({
  label,
  error,
  helpText,
  fullWidth = false,
  className = '',
  id,
  ...props
}) => {
  const inputId = id || `input-${Math.random().toString(36).substring(2, 9)}`;
  
  const baseClasses = 'rounded border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors';
  const errorClasses = error 
    ? 'border-red-500 bg-red-50 focus:ring-red-500' 
    : 'border-gray-300 focus:border-blue-500';
  
  const classes = [
    baseClasses,
    errorClasses,
    fullWidth ? 'w-full' : '',
    className
  ].join(' ');
  
  return (
    <div className={`${fullWidth ? 'w-full' : ''} mb-4`}>
      {label && (
        <label 
          htmlFor={inputId} 
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          {label}
        </label>
      )}
      
      <input 
        id={inputId}
        className={classes}
        {...props}
      />
      
      {helpText && !error && (
        <p className="mt-1 text-sm text-gray-500">{helpText}</p>
      )}
      
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};

export default Input; 