import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

function LogoutButton() {
  const { logout } = useContext(AuthContext);
  
  const handleLogout = async () => {
    try {
      await logout();
      // Optional: Add success notification or redirect
    } catch (error) {
      
      // Optional: Show error message to user
    }
  };

  return (
    <button 
      onClick={handleLogout}
      className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
    >
      Logout
    </button>
  );
}

export default LogoutButton;