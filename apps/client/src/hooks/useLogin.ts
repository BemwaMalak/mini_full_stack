import { useState } from 'react';
import { loginUser, LoginCredentials } from '../services/authService';
import { RESPONSE_MESSAGES } from '../constants/responseMessages';
import { toast } from 'react-toastify';

export const useLogin = () => {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const login = async (credentials: LoginCredentials) => {
    setError(null);
    setLoading(true);
    try {
      const response = await loginUser(credentials);
      if (!response.ok) {
        const errorData = await response.json();
        const errorCode: string = errorData.code || 'E000'; // Default to E001 if code not present
        const errorMessage = RESPONSE_MESSAGES[errorCode];
        throw new Error(errorMessage);
      }

      toast.success(RESPONSE_MESSAGES['S001']);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
        toast.error(err.message);
      } else {
        setError(RESPONSE_MESSAGES['E000']);
        toast.error(RESPONSE_MESSAGES['E000']);
      }
    } finally {
      setLoading(false);
    }
  };

  return { login, error, loading };
};
