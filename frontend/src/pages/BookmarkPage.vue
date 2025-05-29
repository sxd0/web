<template>
  <main class="w-full px-4 md:px-12 lg:px-32 xl:px-64 space-y-6">
    <h1 class="text-2xl font-bold mb-4">⭐ Мои закладки</h1>

    <div v-if="bookmarks.length === 0" class="text-gray-400">
      У вас пока нет закладок.
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="bookmark in bookmarks"
        :key="bookmark.id"
        @click="goToPost(bookmark.post.id)"
        class="bg-gray-800 hover:bg-gray-700 p-4 rounded-lg shadow cursor-pointer"
      >
        <h3 class="font-semibold text-lg mb-1">{{ bookmark.post.title }}</h3>
        <p class="text-gray-400 text-sm truncate">{{ bookmark.post.body }}</p>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const bookmarks = ref([])

const goToPost = (postId) => {
  router.push(`/posts/${postId}`)
}

const loadBookmarks = async () => {
  try {
    const response = await axios.get('http://localhost:8000/bookmarks/my', { withCredentials: true })
    bookmarks.value = response.data
  } catch (err) {
    console.error('Ошибка при загрузке закладок', err)
  }
}

onMounted(() => {
  loadBookmarks()
})
</script>
