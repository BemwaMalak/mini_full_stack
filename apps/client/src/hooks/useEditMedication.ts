import { useState } from 'react';
import {
  updateMedication,
  UpdateMedicationPayload,
} from '../services/medicationService';
import { RESPONSE_MESSAGES } from '../constants/responseMessages';
import { toast } from 'react-toastify';

export const useEditMedication = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleEditMedication = async (
    id: number,
    data: UpdateMedicationPayload,
  ) => {
    setLoading(true);
    setError(null);

    try {
      const response = await updateMedication(id, data);

      if (response.ok) {
        toast.success(RESPONSE_MESSAGES['MEDICATION_UPDATED']);
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

  return { editMedication: handleEditMedication, loading, error };
};
