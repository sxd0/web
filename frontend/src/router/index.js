import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import PostPage from '../pages/PostPage.vue'
import LoginPage from '../pages/LoginPage.vue'
import CreateQuestionPage from '../pages/CreateQuestionPage.vue'
import EditQuestionPage from '../pages/EditQuestionPage.vue'


const routes = [
  { path: '/', component: HomePage },
  { path: '/posts/:id', component: PostPage },
  { path: '/login', component: LoginPage },
  { path: '/create', component: CreateQuestionPage },
  { path: '/posts/:id/edit', component: EditQuestionPage },

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
