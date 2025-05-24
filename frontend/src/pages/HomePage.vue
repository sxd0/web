<template>
  <div class="flex flex-col lg:flex-row gap-6 px-4 md:px-12 lg:px-24 xl:px-32">
    <section class="flex-1 space-y-6">
      <div class="flex gap-4">
        <input
          v-model="searchQuery"
          @keyup.enter="performSearch"
          type="text"
          placeholder="Поиск по вопросам..."
          class="flex-1 p-3 bg-gray-800 border border-gray-600 rounded text-white"
        />
        <button
          @click="performSearch"
          class="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded text-white"
        >
          Найти
        </button>
      </div>

      <div v-if="searchResults.length > 0">
        <h2 class="text-xl font-semibold mb-2">🔍 Результаты поиска</h2>
        <div class="space-y-4">
          <div
            v-for="post in searchResults"
            :key="post.id"
            @click="goToPost(post.id)"
            class="bg-gray-800 hover:bg-gray-700 p-4 rounded-lg shadow cursor-pointer"
          >
            <div class="flex flex-wrap gap-2 mb-2">
              <span
                v-for="tag in post.tags"
                :key="tag"
                @click.stop="searchByTag(tag)"
                class="bg-gray-700 px-2 py-1 rounded-full text-sm cursor-pointer hover:bg-gray-600"
              >
                #{{ tag }}
              </span>
            </div>
            <h3 class="font-semibold text-lg mb-1">{{ post.title }}</h3>
            <p class="text-gray-400 text-sm truncate">{{ post.body }}</p>
          </div>
        </div>
      </div>

      <p v-else-if="searchQuery && searchPerformed" class="text-gray-400">Ничего не найдено.</p>

      <div v-else>
        <h2 class="text-xl font-semibold mb-2">🧠 Популярные вопросы</h2>
        <div class="space-y-4">
          <div
            v-for="post in topPosts"
            :key="post.id"
            @click="goToPost(post.id)"
            class="bg-gray-800 hover:bg-gray-700 p-4 rounded-lg shadow cursor-pointer"
          >
            <div class="flex flex-wrap gap-2 mb-2">
              <span
                v-for="tag in post.tags"
                :key="tag"
                @click.stop="searchByTag(tag)"
                class="bg-gray-700 px-2 py-1 rounded-full text-sm cursor-pointer hover:bg-gray-600"
              >
                #{{ tag }}
              </span>
            </div>
            <h3 class="font-semibold text-lg mb-1">{{ post.title }}</h3>
            <p class="text-gray-400 text-sm truncate">{{ post.body }}</p>
          </div>
        </div>
      </div>
    </section>

    <aside class="w-full lg:w-1/3 space-y-6">
      <Widget title="🔥 Топ посты">
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

      <Widget title="🕒 Последние вопросы">
        <ul class="space-y-2">
          <li class="hover:bg-gray-700 p-2 rounded cursor-pointer">Вопрос 1</li>
          <li class="hover:bg-gray-700 p-2 rounded cursor-pointer">Вопрос 2</li>
        </ul>
      </Widget>

      <Widget title="🏷️ Популярные теги">
        <div class="flex flex-wrap gap-2">
          <span
            v-for="tag in ['vue', 'fastapi', 'sqlalchemy']"
            :key="tag"
            @click="searchByTag(tag)"
            class="bg-gray-700 px-2 py-1 rounded-full cursor-pointer hover:bg-gray-600"
          >
            #{{ tag }}
          </span>
        </div>
      </Widget>
    </aside>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Widget from '../components/Widget.vue'
import { fetchTopPosts, searchPosts } from '../services/posts.js'

const router = useRouter()
const topPosts = ref([])
const searchResults = ref([])
const searchQuery = ref('')
const searchPerformed = ref(false)

onMounted(async () => {
  const posts = await fetchTopPosts()
  topPosts.value = posts.slice(0, 10)
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

function searchByTag(tag) {
  searchQuery.value = tag
  performSearch()
}
</script>
