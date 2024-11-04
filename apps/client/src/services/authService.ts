import { AUTH_ENDPOINTS } from '../constants/api';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterCredentials {
  username: string;
  email: string;
  password: string;
  role: string;
}

export const loginUser = async (
  credentials: LoginCredentials,
): Promise<Response> => {
  return fetch(AUTH_ENDPOINTS.LOGIN, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(credentials),
  });
};

export const registerUser = async (
  credentials: RegisterCredentials,
): Promise<Response> => {
  return fetch(AUTH_ENDPOINTS.REGISTER, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(credentials),
  });
};
