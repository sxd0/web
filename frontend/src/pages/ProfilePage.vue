<template>
  <main class="w-full px-4 md:px-12 lg:px-32 xl:px-64 space-y-6">
    <h1 class="text-2xl font-bold">👤 Мой профиль</h1>
    <p class="text-gray-400 mb-4">Пользователь: {{ user?.email }}</p>

    <div v-if="posts.length > 0" class="space-y-4">
      <h2 class="text-lg font-semibold mb-2">Мои вопросы</h2>
      <div
        v-for="post in posts"
        :key="post.id"
        @click="goToPost(post.id)"
        class="bg-gray-800 hover:bg-gray-700 p-4 rounded-lg shadow cursor-pointer"
      >
        <h3 class="font-semibold text-lg mb-1">{{ post.title }}</h3>
        <p class="text-gray-400 text-sm truncate">{{ post.body }}</p>
      </div>
    </div>

    <p v-else class="text-gray-400">У вас ещё нет вопросов.</p>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCurrentUser } from '../services/auth.js'
import { fetchUserPosts } from '../services/posts.js'

const router = useRouter()
const user = ref(null)
const posts = ref([])

onMounted(async () => {
  user.value = await getCurrentUser()
  posts.value = await fetchUserPosts(user.value.id)
})

function goToPost(id) {
  router.push(`/posts/${id}`)
}
</script>
