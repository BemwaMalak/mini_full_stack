import { useState, useEffect, useRef } from 'react';
import { fetchMedications, Medication } from '../services/medicationService';
import { RESPONSE_MESSAGES } from '../constants/responseMessages';
import { toast } from 'react-toastify';

export const useFetchMedications = () => {
  const [medications, setMedications] = useState<Medication[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const hasFetched = useRef(false);

  const loadMedications = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetchMedications();
      const data = await response.json();

      if (response.ok) {
        setMedications(data.data as Medication[]);
        if (!hasFetched.current) {
          toast.success(RESPONSE_MESSAGES['S005']);
          hasFetched.current = true;
        }
      } else {
        const errorCode: string = data.code || 'E000';
        throw new Error(RESPONSE_MESSAGES[errorCode]);
      }
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
        toast.error(err.message);
      } else {
        const fallbackError = RESPONSE_MESSAGES['E000'];
        setError(fallbackError);
        toast.error(fallbackError);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMedications();
  }, []);

  return { medications, loading, error };
};
