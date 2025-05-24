<template>
  <main class="w-full px-4 md:px-12 lg:px-32 xl:px-64 space-y-6">
    <h1 class="text-2xl font-bold mb-4">Редактировать вопрос</h1>

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
    <h2 class="font-semibold mb-2">Теги:</h2>
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
      Сохранить
    </button>

    <p v-if="error" class="text-red-400">{{ error }}</p>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchPostDetailed, updateQuestion } from '../services/posts.js'


const selectedTags = ref([])
const customTags = ref('')
const availableTags = ['vue', 'fastapi', 'sqlalchemy', 'backend', 'async']
const route = useRoute()
const router = useRouter()

const title = ref('')
const body = ref('')
const tags = ref('')
const error = ref('')

onMounted(async () => {
  const post = await fetchPostDetailed(route.params.id)
  title.value = post.title
  body.value = post.body
  tags.value = post.tags.join(', ')
})

onMounted(async () => {
  const post = await fetchPostDetailed(route.params.id)
  title.value = post.title
  body.value = post.body
  selectedTags.value = post.tags
})

async function submit() {
  try {
    const userTags = customTags.value
    .split(',')
    .map(t => t.trim())
    .filter(t => t)

    const allTags = [...selectedTags.value, ...userTags]
    await updateQuestion(route.params.id, title.value, body.value, allTags)

    router.push(`/posts/${route.params.id}`)
  } catch {
    error.value = 'Ошибка при сохранении'
  }
}
</script>
