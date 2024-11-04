import { useState } from 'react';
import { deleteMedication } from '../services/medicationService';
import { RESPONSE_MESSAGES } from '../constants/responseMessages';
import { toast } from 'react-toastify';

export const useDeleteMedication = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDeleteMedication = async (id: number) => {
    setLoading(true);
    setError(null);

    try {
      const response = await deleteMedication(id);

      if (response.ok) {
        toast.success(RESPONSE_MESSAGES['MEDICATION_DELETED']);
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

  return { deleteMedication: handleDeleteMedication, loading, error };
};
