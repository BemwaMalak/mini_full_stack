import { REFILL_REQUEST_ENDPOINTS } from '../constants/api';
import { Medication } from './medicationService';

export interface RefillRequest {
  id: number;
  medication: Medication;
  quantity: number;
  status: string;
  requested_at: string;
}

export const fetchRefillRequests = async (): Promise<Response> => {
  return fetch(REFILL_REQUEST_ENDPOINTS.LIST_CREATE, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
  });
};
export const fetchRefillRequestsAggregate = async (): Promise<Response> => {
  return fetch(REFILL_REQUEST_ENDPOINTS.AGGREGATE, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
  });
};
