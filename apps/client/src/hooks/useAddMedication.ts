import { useState } from 'react';
import {
  createMedication,
  CreateMedicationPayload,
} from '../services/medicationService';
import { RESPONSE_MESSAGES } from '../constants/responseMessages';
import { toast } from 'react-toastify';

export const useAddMedication = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const addMedication = async (medication: CreateMedicationPayload) => {
    setLoading(true);
    setError(null);
    try {
      const response = await createMedication(medication);
      const data = await response.json();

      if (response.ok) {
        toast.success(RESPONSE_MESSAGES['S004']);
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

  return { addMedication, loading, error };
};
