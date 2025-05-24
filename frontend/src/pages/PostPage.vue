<template>
  <main class="container mx-auto p-6">
    <div v-if="post">
      <h1 class="text-2xl font-bold mb-4">{{ post.title }}</h1>
      <p class="text-gray-300">{{ post.body }}</p>
    </div>
    <div v-else>
      <p class="text-gray-500">Загрузка...</p>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchPostById } from '../services/posts.js'

const post = ref(null)
const route = useRoute()

onMounted(async () => {
  const id = route.params.id
  post.value = await fetchPostById(id)
})
</script>
