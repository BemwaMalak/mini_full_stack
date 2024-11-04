import { useEffect, useState, useRef } from 'react';
import { RESPONSE_MESSAGES } from '../constants/responseMessages';
import { toast } from 'react-toastify';
import { fetchRefillRequestsAggregate } from '../services/refillRequestsService';

interface RefillRequestAggregate {
  name: string;
  refill_request_count: number;
}

export const useRefillRequestAggregate = () => {
  const [data, setData] = useState<RefillRequestAggregate[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const isToastShown = useRef(false); // Track if success toast has been shown

  useEffect(() => {
    const fetchAggregateData = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetchRefillRequestsAggregate();

        if (response.ok) {
          const result = await response.json();
          setData(result.data);

          // Show success toast only once
          if (!isToastShown.current) {
            toast.success(RESPONSE_MESSAGES['S013']);
            isToastShown.current = true; // Mark toast as shown
          }
        } else {
          const errorData = await response.json();
          const errorCode = errorData.code || 'E000';
          const errorMessage = RESPONSE_MESSAGES[errorCode];
          setError(errorMessage);
          toast.error(errorMessage);
        }
      } catch {
        setError(RESPONSE_MESSAGES['E000']);
        toast.error(RESPONSE_MESSAGES['E000']);
      } finally {
        setLoading(false);
      }
    };

    fetchAggregateData();
  }, []);

  return { data, loading, error };
};
