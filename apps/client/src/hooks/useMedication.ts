import { useState, useEffect } from 'react';
import {
  fetchMedications,
  createMedication,
  Medication,
  CreateMedicationPayload,
} from '../services/medicationService';
import { RESPONSE_MESSAGES } from '../constants/responseMessages';
import { toast } from 'react-toastify';

export const useMedications = () => {
  const [medications, setMedications] = useState<Medication[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const loadMedications = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetchMedications();
      const data = await response.json();

      if (response.ok) {
        setMedications(data.data as Medication[]);
        const successMessage = RESPONSE_MESSAGES['S005'];
        toast.success(successMessage);
      } else {
        const errorCode: string = data.code || 'E000';
        const errorMessage = RESPONSE_MESSAGES[errorCode];
        throw new Error(errorMessage);
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

  const addMedication = async (medication: CreateMedicationPayload) => {
    setLoading(true);
    setError(null);
    try {
      const response = await createMedication(medication);
      const data = await response.json();

      if (response.ok) {
        setMedications((prev) => [...prev, data.data as Medication]);
        const successMessage = RESPONSE_MESSAGES['S004'];
        toast.success(successMessage);
      } else {
        const errorCode: string = data.code || 'E000';
        const errorMessage = RESPONSE_MESSAGES[errorCode];
        throw new Error(errorMessage);
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

  return {
    medications,
    loading,
    error,
    reload: loadMedications,
    addMedication,
  };
};
