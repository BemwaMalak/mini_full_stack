import { useState, useEffect } from 'react';
import { AUTH_ENDPOINTS } from '../constants/api';
import { RESPONSE_MESSAGES } from '../constants/responseMessages';

interface User {
  username: string;
  email: string;
  role: string;
}

interface UseAuthReturn {
  isAuthenticated: boolean;
  user: User | null;
  loading: boolean;
  error: unknown | null;
}

export const useAuth = (): UseAuthReturn => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUserInfo = async () => {
      setError(null);
      try {
        const response = await fetch(AUTH_ENDPOINTS.USER_INFO, {
          method: 'GET',
          credentials: 'include',
        });

        if (response.ok) {
          const data = await response.json();
          setUser(data.data);
          setIsAuthenticated(true);
        } else {
          const errorData = await response.json();
          const errorCode = errorData.code || 'E000'; // Default to E000 for unknown errors
          setError(RESPONSE_MESSAGES[errorCode] || RESPONSE_MESSAGES['E000']);
          setIsAuthenticated(false);
          setUser(null);
        }
      } catch {
        setError(RESPONSE_MESSAGES['E000']);
        setIsAuthenticated(false);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    fetchUserInfo();
  }, []);

  return { isAuthenticated, user, loading, error };
};
