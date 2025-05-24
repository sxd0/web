<template>
  <header class="w-full bg-gray-900 px-6 py-3 shadow mb-6">
    <nav class="max-w-7xl mx-auto flex justify-between items-center">
      <div
        @click="goHome"
        class="text-xl font-bold text-green-400 cursor-pointer"
      >
        QueStudio
      </div>
      <div class="space-x-4">
        <router-link to="/" class="hover:text-green-400">Главная</router-link>
        <router-link to="/create" class="hover:text-green-400">Создать</router-link>
        <router-link to="/profile" class="hover:text-green-400">Профиль</router-link>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
function goHome() {
  router.push('/')
}
</script>
