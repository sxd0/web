import api from './api'

export async function login(email, password) {
  const response = await api.post('/auth/login', { email, password }, { withCredentials: true })
  return response.data
}

export async function getCurrentUser() {
  const response = await api.get('/auth/me', { withCredentials: true })
  return response.data
}

export async function refreshToken() {
  const response = await api.post('/auth/refresh', null, { withCredentials: true })
  return response.data
}

export async function logout() {
  const response = await api.post('/auth/logout', null, { withCredentials: true })
  return response.data
}
