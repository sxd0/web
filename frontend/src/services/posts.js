import api from './api'

export async function fetchTopPosts() {
  const response = await api.get('/posts')
  return response.data
}
