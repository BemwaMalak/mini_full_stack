import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from 'react-router-dom';
import Login from './pages/Login/Login';
import Register from './pages/Register/Register';
import Home from './pages/Home/Home';
import ProtectedRoute from './components/ProtectedRoute/ProtectedRoute';
import AdminProtectedRoute from './components/AdminProtectedRoute/AdminProtectedRoute';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Spinner from './components/Spinner/Spinner';
import { useAuth } from './hooks/useAuth';
import AddMedication from './pages/AddMedication/AddMedication';
import MyRequestsPage from './pages/MyRequests/MyRequests';
import DashboardPage from './pages/Dashboard/Dashboard';

function App(): React.JSX.Element {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <Spinner loading={loading} />;
  }

  return (
    <Router>
      <ToastContainer position="top-right" autoClose={5000} hideProgressBar />
      <Routes>
        <Route
          path="/login"
          element={
            isAuthenticated ? <Navigate to="/home" replace /> : <Login />
          }
        />
        <Route
          path="/register"
          element={
            <AdminProtectedRoute>
              <Register />
            </AdminProtectedRoute>
          }
        />
        <Route
          path="/my-requests"
          element={
            <ProtectedRoute>
              <MyRequestsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/dashboard"
          element={
            <AdminProtectedRoute>
              <DashboardPage />
            </AdminProtectedRoute>
          }
        />
        <Route
          path="/add-medication"
          element={
            <AdminProtectedRoute>
              <AddMedication />
            </AdminProtectedRoute>
          }
        />
        <Route
          path="/home"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
        <Route
          path="/"
          element={
            isAuthenticated ? (
              <Navigate to="/home" replace />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
