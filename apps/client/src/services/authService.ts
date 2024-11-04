import { API_URLS } from '../constants/api';

export interface LoginCredentials {
  username: string;
  password: string;
}

export const loginUser = async (
  credentials: LoginCredentials,
): Promise<Response> => {
  return fetch(API_URLS.LOGIN, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(credentials),
  });
};
