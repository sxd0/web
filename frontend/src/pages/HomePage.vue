<template>
  <main class="container mx-auto p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <Widget title="🔥 Топ посты">
      <ul class="space-y-2">
        <li
          v-for="post in topPosts"
          :key="post.id"
          class="hover:bg-gray-700 p-2 rounded cursor-pointer"
        >
          {{ post.title }}
        </li>
      </ul>
    </Widget>

    <Widget title="🕒 Последние вопросы">
      <ul class="space-y-2">
        <li class="hover:bg-gray-700 p-2 rounded cursor-pointer">Вопрос 1</li>
        <li class="hover:bg-gray-700 p-2 rounded cursor-pointer">Вопрос 2</li>
      </ul>
    </Widget>

    <Widget title="🏷️ Популярные теги">
      <ul class="space-y-2">
        <li class="hover:bg-gray-700 p-2 rounded cursor-pointer">#vue</li>
        <li class="hover:bg-gray-700 p-2 rounded cursor-pointer">#fastapi</li>
      </ul>
    </Widget>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Widget from '../components/Widget.vue'
import { fetchTopPosts } from '../services/posts.js'

const topPosts = ref([])

onMounted(async () => {
  const posts = await fetchTopPosts()
  topPosts.value = posts.slice(0, 5)
})
</script>
