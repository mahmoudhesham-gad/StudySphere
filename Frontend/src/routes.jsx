// src/routes.jsx
import { createBrowserRouter, Navigate, Outlet } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from './features/auth/AuthContext';
import Loading  from './components/ui/Loading';

// Import your page components
import Login from './pages/users/Login';
import Register from './pages/users/Register';
import NotFound from './pages/users/NotFound';
import Layout from './components/Layout/Layout'
import Profile from './pages/users/Profile';
import Home from './pages/Home';

// Protected route wrapper
const ProtectedRoute = () => {
  const { isAuthenticated, loading } = useContext(AuthContext);
  
  if (loading) {
    return <Loading size="lg" fullScreen text="Loading your profile..." />;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};

// Public route wrapper (redirects if already authenticated)
const PublicRoute = () => {
  const { isAuthenticated, loading } = useContext(AuthContext);
  
  if (loading) {
    return <Loading size="lg" fullScreen text="Please wait..." />;
  }
  
  if (isAuthenticated) {
    return <Navigate to="/profile" replace />;
  }

  return <Outlet />;
};

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      {
        index: true,
        element: <Home />
      },
      {
        element: <PublicRoute />,
        children: [
          {
            path: 'login/',
            element: <Login />
          },
          {
            path: 'register/',
            element: <Register />
          }
        ]
      },
      {
        element: <ProtectedRoute />,
        children: [
          {
            path: 'profile',
            element: <Profile />
          }
        ]
      },
      {
        path: '*',
        element: <NotFound />
      }
    ]
  }
]);