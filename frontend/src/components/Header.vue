<template>
  <header class="w-full bg-gray-900 px-6 py-3 shadow mb-6">
    <nav class="max-w-7xl mx-auto flex justify-between items-center">
      <div
        @click="goHome"
        class="text-xl font-bold text-green-400 cursor-pointer"
      >
        QueStudio
      </div>
      <div class="space-x-4 flex items-center">
        <router-link to="/" class="hover:text-green-400">Главная</router-link>
        <router-link to="/create" class="hover:text-green-400">Создать</router-link>

        <template v-if="user">
          <span class="text-sm text-gray-400">{{ user.username }}</span>
          <button @click="handleLogout" class="text-red-400 hover:text-red-300 text-sm">Выйти</button>
        </template>

        <template v-else>
          <router-link to="/login" class="hover:text-green-400">Войти</router-link>
        </template>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { logout } from '../services/auth.js'
import { useAuth } from '../stores/authStore.js'

const router = useRouter()
const { user, fetchUser } = useAuth()

fetchUser()

function goHome() {
  router.push('/')
}

async function handleLogout() {
  await logout()
  await fetchUser()
  router.push('/')
}
</script>
