import axios from 'axios'

export async function toggleBookmark(postId, isBookmarked) {
  try {
    if (isBookmarked) {
      await axios.delete(`http://localhost:8000/bookmarks/${postId}`, { withCredentials: true })
      return false
    } else {
      await axios.post(`http://localhost:8000/bookmarks/`, { post_id: postId }, { withCredentials: true })
      return true
    }
  } catch (err) {
    console.error('Ошибка при обновлении закладки', err)
    return isBookmarked
  }
}
