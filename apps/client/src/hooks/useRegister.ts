import { useState } from 'react';
import { registerUser, RegisterCredentials } from '../services/authService';
import { RESPONSE_MESSAGES } from '../constants/responseMessages';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';

export const useRegister = () => {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const navigate = useNavigate();

  const register = async (credentials: RegisterCredentials): Promise<void> => {
    setError(null);
    setLoading(true);
    try {
      const response = await registerUser(credentials);
      if (!response.ok) {
        const errorData = await response.json();
        const errorCode: string = errorData.code || 'E000';
        const errorMessage = RESPONSE_MESSAGES[errorCode];
        throw new Error(errorMessage);
      }

      toast.success(RESPONSE_MESSAGES['S003']);
      // Optionally, navigate to login page or dashboard
      navigate('/login');
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

  return { register, error, loading };
};
