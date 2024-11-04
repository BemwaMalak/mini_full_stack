import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import Spinner from '../Spinner/Spinner';

interface ProtectedRouteProps {
  children: React.JSX.Element;
}

const AdminProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, user, loading } = useAuth();

  if (loading) {
    return <Spinner loading={loading} />;
  }

  if (!isAuthenticated || user?.role !== 'ADMIN') {
    return <Navigate to="/home" replace />;
  }

  return children;
};

export default AdminProtectedRoute;
