<template>
  <main class="container mx-auto p-6 space-y-6">
    <div class="flex items-center gap-4">
      <input
        v-model="searchQuery"
        @keyup.enter="performSearch"
        type="text"
        placeholder="Поиск по вопросам..."
        class="flex-1 p-2 bg-gray-700 border border-gray-600 rounded text-white"
      />
      <button @click="performSearch" class="px-4 py-2 bg-gray-600 rounded hover:bg-gray-500">
        Найти
      </button>
    </div>

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

    <Widget v-if="searchResults.length > 0" title="🔎 Результаты поиска">
      <ul class="space-y-2">
        <li
          v-for="post in topPosts"
          :key="post.id"
          @click="goToPost(post.id)"
          class="hover:bg-gray-700 p-2 rounded cursor-pointer"
        >
          {{ post.title }}
        </li>
      </ul>
    </Widget>

    <Widget v-else-if="searchQuery && searchPerformed" title="🔎 Результаты поиска">
      <p class="text-gray-400">Ничего не найдено</p>
    </Widget>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Widget from '../components/Widget.vue'
import { fetchTopPosts, searchPosts } from '../services/posts.js'
import { useRouter } from 'vue-router'


const router = useRouter()
const topPosts = ref([])
const searchResults = ref([])
const searchQuery = ref('')
const searchPerformed = ref(false)

onMounted(async () => {
  const posts = await fetchTopPosts()
  topPosts.value = posts.slice(0, 5)
})

async function performSearch() {
  searchPerformed.value = true
  if (searchQuery.value.trim()) {
    const results = await searchPosts(searchQuery.value)
    searchResults.value = results
  } else {
    searchResults.value = []
  }
}

function goToPost(id) {
  router.push(`/posts/${id}`)
}

</script>
