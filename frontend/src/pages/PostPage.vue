<template>
  <main class="container mx-auto p-6 space-y-4">
    <div v-if="post">
      <h1 class="text-2xl font-bold mb-2">{{ post.title }}</h1>
      <p class="text-gray-300 mb-4">{{ post.body }}</p>

      <div class="text-sm text-gray-400 space-y-1">
        <div>👁️ Просмотры: {{ post.views }}</div>
        <div>🗳️ Голоса: {{ post.votes }}</div>
        <div>📅 Дата публикации: {{ formatDate(post.created_at) }}</div>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="tag in post.tags"
            :key="tag"
            class="bg-gray-700 px-2 py-1 rounded-full text-sm"
          >
            #{{ tag }}
          </span>
        </div>
      </div>
    </div>

    <div v-else>
      <p class="text-gray-500">Загрузка...</p>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchPostDetailed } from '../services/posts.js'

const post = ref(null)
const route = useRoute()

onMounted(async () => {
  const id = route.params.id
  post.value = await fetchPostDetailed(id)
})

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleString()
}
</script>
