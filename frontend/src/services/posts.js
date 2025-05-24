import api from './api'

export async function fetchTopPosts() {
  const response = await api.get('/posts')
  return response.data
}

export async function searchPosts(query) {
  const response = await api.get('/posts', {
    params: { search: query }
  })
  return response.data
}

export async function fetchPostById(id) {
  const response = await api.get(`/posts/${id}`)
  return response.data
}

export async function fetchPostDetailed(id) {
  const response = await api.get(`/posts/${id}/detailed`)
  return response.data
}
