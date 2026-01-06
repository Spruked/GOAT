import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');

  if (!token) {
    // Redirect to login with return url
    return <Navigate to="/login" state={{ from: window.location.pathname }} replace />;
  }

  return children;
};

export default ProtectedRoute;