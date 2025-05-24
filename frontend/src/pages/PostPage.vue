<template>
  <main class="w-full px-4 md:px-12 lg:px-32 xl:px-64 space-y-6">
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

    <!-- 💬 Форма ответа -->
    <div class="mt-8">
      <h2 class="text-xl font-semibold mb-2">Оставить ответ</h2>
      <textarea
        v-model="answerText"
        rows="5"
        placeholder="Ваш ответ..."
        class="w-full p-3 bg-gray-800 border border-gray-600 rounded text-white"
      ></textarea>
      <button
        @click="submitAnswer"
        class="mt-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded"
      >
        Отправить
      </button>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchPostDetailed, createAnswer } from '../services/posts.js'

const post = ref(null)
const route = useRoute()
const answerText = ref('')

onMounted(async () => {
  const id = route.params.id
  post.value = await fetchPostDetailed(id)
})

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleString()
}

async function submitAnswer() {
  if (!answerText.value.trim()) return
  const id = route.params.id
  await createAnswer(answerText.value, id)
  answerText.value = ''
  location.reload()
}
</script>
