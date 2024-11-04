export const API_BASE_URL = import.meta.env.VITE_API_URL;

export const AUTH_ENDPOINTS = {
  LOGIN: `${API_BASE_URL}/auth/login/`,
  LOGOUT: `${API_BASE_URL}/auth/logout/`,
  REGISTER: `${API_BASE_URL}/auth/register/`,
  USER_INFO: `${API_BASE_URL}/auth/user-info/`,
};

export const MEDICATION_ENDPOINTS = {
  LIST_CREATE: `${API_BASE_URL}/medication/`,
  DETAIL_UPDATE: (pk: number) => `${API_BASE_URL}/medication/${pk}/`,
};

export const REFILL_REQUEST_ENDPOINTS = {
  LIST_CREATE: `${API_BASE_URL}/medication/refill-request/`,
  DETAIL_UPDATE: (pk: number) =>
    `${API_BASE_URL}/medication/refill-request/${pk}/`,
  AGGREGATE: `${API_BASE_URL}/medication/refill-request/aggregate/`,
};
