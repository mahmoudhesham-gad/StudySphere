import React from 'react';

/**
 * Loading component with different size and color options
 * 
 * @param {Object} props
 * @param {'sm'|'md'|'lg'|'xl'} [props.size='md'] - Size of the spinner
 * @param {string} [props.color='primary'] - Color variant (primary, secondary, success, danger, warning)
 * @param {boolean} [props.fullScreen=false] - Whether the spinner should be centered on the full screen
 * @param {string} [props.text] - Optional text to display below the spinner
 */
const Loading = ({ 
  size = 'md', 
  color = 'primary', 
  fullScreen = false,
  text
}) => {
  // Size classes mapping
  const sizeClasses = {
    sm: 'w-5 h-5 border-2',
    md: 'w-8 h-8 border-3',
    lg: 'w-12 h-12 border-4',
    xl: 'w-16 h-16 border-4'
  };
  
  // Color classes mapping
  const colorClasses = {
    primary: 'border-blue-600 border-t-transparent',
    secondary: 'border-gray-600 border-t-transparent',
    success: 'border-green-600 border-t-transparent',
    danger: 'border-red-600 border-t-transparent',
    warning: 'border-yellow-500 border-t-transparent',
  };
  
  const spinnerClasses = `
    ${sizeClasses[size] || sizeClasses.md}
    ${colorClasses[color] || colorClasses.primary}
    rounded-full animate-spin
  `;
  
  const loadingContent = (
    <div className="flex flex-col items-center justify-center">
      <div className={spinnerClasses}></div>
      {text && <p className="mt-3 text-gray-600">{text}</p>}
    </div>
  );
  
  if (fullScreen) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-white bg-opacity-75 z-50">
        {loadingContent}
      </div>
    );
  }
  
  return loadingContent;
};

export default Loading;
