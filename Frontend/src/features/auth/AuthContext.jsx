// src/context/AuthContext.jsx
import React, { createContext, useState, useEffect } from 'react';
import { authService } from './authService';
import { userService } from '../user/userService';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const userResponse = await userService.getCurrentUser();
        setUser(userResponse.data);
      } catch (e) {
        try {
          // If getting user fails, try to verify and refresh it
          await authService.verify();
          await authService.refreshToken();

          const userResponse = await userService.getCurrentUser();
          setUser(userResponse.data);
        } catch (verifyError) {
          setUser(null);
        };
      } finally {
        setLoading(false);
      };
    };

    checkAuth();
  }, []);

  const login = async (credentials) => {
    const response = await authService.login(credentials);
    const userResponse = await userService.getCurrentUser();
    setUser(userResponse.data);
    return response;
  };

  const logout = async () => {
    try {
      await authService.logout();
      setUser(null);
    }
    catch (e) {
      console.error('Logout error:', e);
    }
  };

  return (
    <AuthContext.Provider value={{ 
      user, 
      isAuthenticated: user !== null, 
      login, 
      logout, 
      loading 
    }}>
      {children}
    </AuthContext.Provider>
  );
};