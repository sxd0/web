<template>
  <main class="w-full px-4 md:px-12 lg:px-32 xl:px-64 space-y-6">
    <h1 class="text-2xl font-bold">Вход</h1>

    <input
      v-model="email"
      type="email"
      placeholder="Email"
      class="w-full p-3 bg-gray-800 border border-gray-600 rounded text-white"
    />

    <input
      v-model="password"
      type="password"
      placeholder="Пароль"
      class="w-full p-3 bg-gray-800 border border-gray-600 rounded text-white"
    />

    <button
      @click="submit"
      class="px-6 py-2 bg-blue-600 hover:bg-blue-500 rounded"
    >
      Войти
    </button>

    <p v-if="error" class="text-red-400">{{ error }}</p>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login, getCurrentUser } from '../services/auth.js'
import { useAuth } from '../stores/authStore.js'


const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()
const { fetchUser } = useAuth()


async function submit() {
  try {
    await login(email.value, password.value)
    await fetchUser()
    await getCurrentUser()
    router.push('/')
  } catch (e) {
    error.value = 'Неверные данные'
  }
}
</script>
