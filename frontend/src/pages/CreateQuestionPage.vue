<template>
  <main class="w-full px-4 md:px-12 lg:px-32 xl:px-64 space-y-6">
    <h1 class="text-2xl font-bold mb-4">Создать вопрос</h1>

    <input
      v-model="title"
      type="text"
      placeholder="Заголовок"
      class="w-full p-3 bg-gray-800 border border-gray-600 rounded text-white"
    />

    <textarea
      v-model="body"
      rows="6"
      placeholder="Текст вопроса"
      class="w-full p-3 bg-gray-800 border border-gray-600 rounded text-white"
    ></textarea>

    <div>
      <h2 class="font-semibold mb-2">Выберите теги:</h2>
      <div class="flex flex-wrap gap-3">
        <label
          v-for="tag in availableTags"
          :key="tag"
          class="flex items-center gap-2 text-sm bg-gray-800 px-3 py-1 rounded"
        >
          <input
            type="checkbox"
            :value="tag"
            v-model="selectedTags"
            class="accent-green-500"
          />
          {{ tag }}
        </label>
      </div>
    </div>

    <input
      v-model="customTags"
      type="text"
      placeholder="Добавить свои теги (через запятую)"
      class="w-full p-3 bg-gray-800 border border-gray-600 rounded text-white"
    />

    <button
      @click="submit"
      class="px-6 py-2 bg-blue-600 hover:bg-blue-500 rounded"
    >
      Опубликовать
    </button>

    <p v-if="error" class="text-red-400">{{ error }}</p>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { createQuestion } from '../services/posts.js'

const router = useRouter()
const title = ref('')
const body = ref('')
const selectedTags = ref([])
const customTags = ref('')
const error = ref('')
const availableTags = ['vue', 'fastapi', 'sqlalchemy', 'async', 'backend']

async function submit() {
  try {
    const userTags = customTags.value
      .split(',')
      .map(t => t.trim())
      .filter(t => t)
    const allTags = [...selectedTags.value, ...userTags]
    const post = await createQuestion(title.value, body.value, allTags)
    router.push(`/posts/${post.id}`)
  } catch (e) {
    error.value = 'Ошибка при создании'
  }
}
</script>
