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
            <h3 class="font-semibold text-lg mb-1 flex items-center gap-2">
              {{ post.title }}
              <span
                @click.stop="toggleBookmark(post)"
                class="cursor-pointer text-yellow-400 text-xl"
              >
                <span v-if="post.is_bookmarked">★</span>
                <span v-else>☆</span>
              </span>
            </h3>


            <p class="text-gray-400 text-sm truncate">{{ post.body }}</p>
          </div>
        </div>
      </div>

      <p v-else-if="searchQuery && searchPerformed" class="text-gray-400">Ничего не найдено.</p>

      <div v-else>
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4">
          <h2 class="text-xl font-semibold">🧠 Популярные вопросы</h2>
          <div class="flex items-center gap-3">
            <label class="text-gray-400">Сортировать:</label>
            <select v-model="sortOption" @change="loadPosts" class="bg-gray-800 border border-gray-600 rounded px-2 py-1 text-white">
              <option value="new">По дате</option>
              <option value="popular">По популярности</option>
            </select>
            <div v-if="activeTag">
              <span class="text-sm text-green-400">Тег: #{{ activeTag }}</span>
              <button @click="clearTag" class="ml-2 text-red-400 text-sm hover:underline">Сбросить</button>
            </div>
          </div>
        </div>

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
            <h3 class="font-semibold text-lg mb-1 flex items-center gap-2">
              {{ post.title }}
              <span
                @click.stop="toggleBookmark(post)"
                class="text-yellow-400 cursor-pointer text-xl"
              >
                <span v-if="post.is_bookmarked">★</span>
                <span v-else>☆</span>
              </span>
            </h3>


            <p class="text-gray-400 text-sm truncate">{{ post.body }}</p>
          </div>
        </div>
      <div class="flex justify-between items-center mt-6">
        <button
          :disabled="page === 1"
          @click="() => { page--; loadPosts() }"
          class="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded disabled:opacity-40"
        >
          ⬅️ Назад
        </button>

        <span class="text-gray-400 text-sm">Страница {{ page }}</span>

        <button
          @click="() => { page++; loadPosts() }"
          class="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded"
        >
          Вперёд ➡️
        </button>
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
import { ref, onMounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import Widget from '../components/Widget.vue'
import { fetchTopPosts, searchPosts } from '../services/posts.js'
import axios from 'axios'

const router = useRouter()
const topPosts = ref([])
const searchResults = ref([])
const searchQuery = ref('')
const searchPerformed = ref(false)
const sortOption = ref("new")
const activeTag = ref(null)

const page = ref(1)
const pageSize = 5


onMounted(() => {
  loadPosts()
})


watch(
  () => router.fullPath,
  (newPath) => {
    if (newPath.startsWith('/')) {
      searchQuery.value = ''
      searchResults.value = []
      searchPerformed.value = false
      loadPosts()
    }
  }
)


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
  activeTag.value = tag
  page.value = 1
  loadPosts()
}

function clearTag() {
  activeTag.value = null
  page.value = 1
  loadPosts()
}


async function loadPosts() {
  const posts = await fetchTopPosts({
    sort: sortOption.value,
    tag: activeTag.value,
    limit: pageSize,
    offset: (page.value - 1) * pageSize
  })

  if (posts.length === 0 && page.value > 1) {
    page.value--
    return
  }

  topPosts.value = posts

}


const toggleBookmark = async (post) => {
  try {
    if (post.is_bookmarked) {
      await axios.delete(`http://localhost:8000/bookmarks/${post.id}`, {
        withCredentials: true
      })
      post.is_bookmarked = false
    } else {
      await axios.post(
        `http://localhost:8000/bookmarks/`,
        { post_id: post.id },
        { withCredentials: true }
      )
      post.is_bookmarked = true
    }
  } catch (err) {
    console.error('Ошибка при переключении закладки', err)
  }
}



async function handleBookmarkToggle(post) {
  post.is_bookmarked = await toggleBookmark(post.id, post.is_bookmarked)
}


</script>
