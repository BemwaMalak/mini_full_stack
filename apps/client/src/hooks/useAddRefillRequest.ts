import { useState } from 'react';
import { toast } from 'react-toastify';
import { RESPONSE_MESSAGES } from '../constants/responseMessages';
import { REFILL_REQUEST_ENDPOINTS } from '../constants/api';

interface AddRefillRequestReturn {
  // eslint-disable-next-line no-unused-vars
  addRefillRequest: (medicationId: number, quantity: number) => Promise<void>;
  loading: boolean;
  error: string | null;
}

export const useAddRefillRequest = (): AddRefillRequestReturn => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const addRefillRequest = async (medicationId: number, quantity: number) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(REFILL_REQUEST_ENDPOINTS.LIST_CREATE, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ medication: medicationId, quantity }),
      });

      if (response.ok) {
        toast.success(RESPONSE_MESSAGES['REFILL_REQUEST_CREATED']);
      } else {
        const errorData = await response.json();
        const errorCode = errorData.code || 'E000';
        setError(RESPONSE_MESSAGES[errorCode]);
        toast.error(RESPONSE_MESSAGES[errorCode]);
      }
    } catch {
      setError(RESPONSE_MESSAGES['E000']);
      toast.error(RESPONSE_MESSAGES['E000']);
    } finally {
      setLoading(false);
    }
  };

  return { addRefillRequest, loading, error };
};
