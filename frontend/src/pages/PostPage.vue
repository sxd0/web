<template>
  <main class="w-full px-4 md:px-12 lg:px-32 xl:px-64 space-y-6">
    <div v-if="post">
      <div class="flex items-center gap-4 mb-4">
        <h1 class="text-2xl font-bold flex items-center gap-2">
          {{ post.title }}
          <span @click="toggleBookmark" class="text-yellow-400 cursor-pointer text-xl">
            <span v-if="isBookmarked">★</span>
            <span v-else>☆</span>
          </span>
        </h1>

        <router-link
          v-if="isAuthor"
          :to="`/posts/${post.id}/edit`"
          class="text-blue-400 hover:underline text-sm"
        >
          ✏️ Редактировать
        </router-link>

        <button
          @click="toggleLike"
          class="px-3 py-1 text-sm rounded bg-gray-700 hover:bg-gray-600"
        >
          👍 {{ post.votes }}
        </button>
      </div>

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

    <section v-if="answers.length > 0" class="space-y-4">
      <h2 class="text-xl font-semibold mt-8">Ответы ({{ answers.length }})</h2>
      <div
        v-for="answer in answers"
        :key="answer.id"
        class="bg-gray-800 p-4 rounded-lg border border-gray-700"
      >
        <p class="text-gray-300 mb-2">{{ answer.body }}</p>
        <p class="text-sm text-gray-500">🕓 {{ formatDate(answer.created_at) }}</p>
      </div>
    </section>

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
import { fetchPostDetailed, createAnswer, fetchAnswers } from '../services/posts.js'
import { getMyVote, likePost, unlikePost } from '../services/posts.js'
import { getCurrentUser } from '../services/auth.js'
import axios from 'axios'
import api from '../services/api'
import { toggleBookmark as toggleBookmarkAPI } from '../services/bookmarks'

const post = ref(null)
const answers = ref([])
const route = useRoute()
const answerText = ref('')
const isAuthenticated = ref(false)
const myVote = ref(null)
const isAuthor = ref(false)
const isBookmarked = ref(false)


onMounted(async () => {
  const id = route.params.id
  post.value = await fetchPostDetailed(id)
  isBookmarked.value = response.is_bookmarked
  answers.value = await fetchAnswers(id)

  try {
    await getCurrentUser()
    isAuthenticated.value = true
  } catch {}
})


onMounted(async () => {
  const user = await getCurrentUser()
  isAuthor.value = post.value && post.value.author_id === user.id
})

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleString()
}

async function submitAnswer() {
  if (!isAuthenticated.value || !answerText.value.trim()) return
  const id = route.params.id
  await createAnswer(answerText.value, id)
  answerText.value = ''
  answers.value = await fetchAnswers(id)
}

async function toggleLike() {
  if (!isAuthenticated.value) return

  const id = post.value.id
  if (myVote.value) {
    await unlikePost(id)
    myVote.value = null
  } else {
    await likePost(id)
    myVote.value = { vote_type: 'up' }
  }

  const updated = await fetchPostDetailed(id)
  isBookmarked.value = response.is_bookmarked
  post.value = updated
}

const toggleBookmark = async () => {
  try {
    if (!post.value) return
    const postId = post.value.id
    console.log("Добавляем в закладки пост:", postId)

    if (isBookmarked.value) {
      await api.delete(`/bookmarks/${postId}`)
      isBookmarked.value = false
    } else {
      await api.post(`/bookmarks/`, { post_id: postId })
      isBookmarked.value = true
    }
  } catch (err) {
    console.error('Ошибка при переключении закладки', err)
  }
}






</script>
