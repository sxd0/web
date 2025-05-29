import api from './api'

export async function fetchTopPosts({ sort = 'new', tag = null, limit = 10, offset = 0 }) {
  let url = `/posts?sort=${sort}&limit=${limit}&offset=${offset}`
  if (tag) url += `&tag=${tag}`
  const response = await api.get(url)
  return response.data
}

export async function searchPosts(query) {
  try {
    const response = await api.get('/posts/search', {
      params: { query }
    })
    return response.data
  } catch (err) {
    console.error('Ошибка при поиске:', err)
    return []
  }
}

export async function fetchPostById(id) {
  const response = await api.get(`/posts/${id}`)
  return response.data
}

export async function fetchPostDetailed(id) {
  const response = await api.get(`/posts/${id}/detailed`)
  return response.data
}

export async function createAnswer(body, parentId) {
  const payload = {
    title: 'Ответ',
    body,
    post_type: 'answer',
    parent_id: parseInt(parentId)
  }
  const response = await api.post('/posts', payload)
  return response.data
}

export async function fetchAnswers(postId) {
  const response = await api.get(`/posts/${postId}/answers`)
  return response.data
}

export async function createQuestion(title, body, tags = []) {
  const payload = {
    title,
    body,
    post_type: 'question',
    tags
  }
  const response = await api.post('/posts', payload)
  return response.data
}

export async function getMyVote(postId) {
  const response = await api.get(`/votes/votes/my/${postId}`)
  return response.data
}

export async function likePost(postId) {
  await api.post('/votes', {
    post_id: postId,
    vote_type: 'up'
  })
}

export async function unlikePost(postId) {
  await api.delete('/votes', {
    data: {
      post_id: postId,
      vote_type: 'up'
    }
  })
}

export async function updateQuestion(postId, title, body, tags = []) {
  const payload = {
    title,
    body,
    post_type: 'question',
    tags
  }
  const response = await api.put(`/posts/${postId}`, payload)
  return response.data
}

export async function fetchUserPosts(userId) {
  const response = await api.get(`/posts?author_id=${userId}&limit=100`)
  return response.data
}
