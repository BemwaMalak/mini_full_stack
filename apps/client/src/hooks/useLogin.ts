import { useState } from 'react';
import { loginUser, LoginCredentials } from '../services/authService';
import { ERROR_CODES } from '../constants/errorCodes';

export const useLogin = () => {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const login = async (credentials: LoginCredentials) => {
    setError(null);
    setLoading(true);
    try {
      const response = await loginUser(credentials);
      if (!response.ok) {
        const errorData = await response.json();
        const errorMessage = errorData.message || 'Login failed';

        switch (errorData.code) {
          case ERROR_CODES.ACCOUNT_LOCKED:
            throw new Error(
              'Account is locked due to multiple failed login attempts.',
            );
          case ERROR_CODES.TOO_MANY_REQUESTS:
            throw new Error('Too many login attempts. Please try again later.');
          default:
            throw new Error(errorMessage);
        }
      }
    } catch (error) {
      setError((error as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return { login, error, loading };
};
