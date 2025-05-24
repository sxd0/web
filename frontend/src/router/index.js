import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import PostPage from '../pages/PostPage.vue'

const routes = [
  { path: '/', component: HomePage },
  { path: '/posts/:id', component: PostPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
