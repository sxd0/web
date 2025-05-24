import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import PostPage from '../pages/PostPage.vue'
import LoginPage from '../pages/LoginPage.vue'
import CreateQuestionPage from '../pages/CreateQuestionPage.vue'


const routes = [
  { path: '/', component: HomePage },
  { path: '/posts/:id', component: PostPage },
  { path: '/login', component: LoginPage },
  { path: '/create', component: CreateQuestionPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
