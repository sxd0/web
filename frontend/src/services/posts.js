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
