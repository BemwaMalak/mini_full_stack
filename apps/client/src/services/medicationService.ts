import { MEDICATION_ENDPOINTS } from '../constants/api';

export interface Medication {
  id: number;
  name: string;
  dosage: string;
  quantity: number;
  instructions: string;
  image?: string | null;
  added_by: string;
  created_at: string;
  updated_at: string;
}

export interface CreateMedicationPayload {
  name: string;
  dosage: string;
  quantity: number;
  instructions: string;
  image?: File | null;
}

export interface UpdateMedicationPayload {
  name?: string;
  dosage?: string;
  quantity?: number;
  instructions?: string;
  image?: File | null;
}

export const fetchMedications = async (): Promise<Response> => {
  return fetch(MEDICATION_ENDPOINTS.LIST_CREATE, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
  });
};

export const fetchMedicationById = async (id: number): Promise<Response> => {
  return fetch(MEDICATION_ENDPOINTS.DETAIL_UPDATE(id), {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
  });
};

export const createMedication = async (
  medication: CreateMedicationPayload,
): Promise<Response> => {
  if (medication.image) {
    const formData = new FormData();
    formData.append('name', medication.name);
    formData.append('dosage', medication.dosage);
    formData.append('quantity', medication.quantity.toString());
    formData.append('instructions', medication.instructions);
    formData.append('image', medication.image);

    return fetch(MEDICATION_ENDPOINTS.LIST_CREATE, {
      method: 'POST',
      credentials: 'include',
      body: formData,
    });
  } else {
    const payload = {
      name: medication.name,
      dosage: medication.dosage,
      quantity: medication.quantity,
      instructions: medication.instructions,
    };

    return fetch(MEDICATION_ENDPOINTS.LIST_CREATE, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(payload),
    });
  }
};

export const updateMedication = async (
  id: number,
  medication: UpdateMedicationPayload,
): Promise<Response> => {
  if (medication.image) {
    const formData = new FormData();
    if (medication.name !== undefined) formData.append('name', medication.name);
    if (medication.dosage !== undefined)
      formData.append('dosage', medication.dosage);
    if (medication.quantity !== undefined)
      formData.append('quantity', medication.quantity.toString());
    if (medication.instructions !== undefined)
      formData.append('instructions', medication.instructions);
    formData.append('image', medication.image);

    return fetch(MEDICATION_ENDPOINTS.DETAIL_UPDATE(id), {
      method: 'PUT',
      credentials: 'include',
      body: formData,
    });
  } else {
    const payload: Partial<CreateMedicationPayload> = {
      name: medication.name,
      dosage: medication.dosage,
      quantity: medication.quantity,
      instructions: medication.instructions,
    };

    return fetch(MEDICATION_ENDPOINTS.DETAIL_UPDATE(id), {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(payload),
    });
  }
};

export const deleteMedication = async (id: number): Promise<Response> => {
  return fetch(MEDICATION_ENDPOINTS.DETAIL_UPDATE(id), {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
  });
};
