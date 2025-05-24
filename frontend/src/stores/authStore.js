import { ref } from 'vue'
import { getCurrentUser, refreshToken } from '../services/auth.js'

const user = ref(null)

async function fetchUser() {
  try {
    user.value = await getCurrentUser()
  } catch {
    try {
      await refreshToken()
      user.value = await getCurrentUser()
    } catch {
      user.value = null
    }
  }
}

export function useAuth() {
  return { user, fetchUser }
}
