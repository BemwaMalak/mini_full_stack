import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { AUTH_ENDPOINTS } from '../constants/api';
import { RESPONSE_MESSAGES } from '../constants/responseMessages';

interface UseLogoutReturn {
  logout: () => Promise<void>;
}

export const useLogout = (): UseLogoutReturn => {
  const navigate = useNavigate();

  const logout = async () => {
    try {
      const response = await fetch(AUTH_ENDPOINTS.LOGOUT, {
        method: 'POST',
        credentials: 'include',
      });

      if (response.ok) {
        toast.success(RESPONSE_MESSAGES['S002']);
        navigate('/login');
      } else {
        const errorData = await response.json();
        const errorCode = errorData.code || 'E000';
        toast.error(RESPONSE_MESSAGES[errorCode]);
      }
    } catch {
      toast.error(RESPONSE_MESSAGES['E000']);
    }
  };

  return { logout };
};
