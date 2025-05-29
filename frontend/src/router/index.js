import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import PostPage from '../pages/PostPage.vue'
import LoginPage from '../pages/LoginPage.vue'
import CreateQuestionPage from '../pages/CreateQuestionPage.vue'
import EditQuestionPage from '../pages/EditQuestionPage.vue'
import ProfilePage from '../pages/ProfilePage.vue'


const routes = [
  { path: '/', component: HomePage },
  { path: '/posts/:id', component: PostPage },
  { path: '/login', component: LoginPage },
  { path: '/create', component: CreateQuestionPage },
  { path: '/posts/:id/edit', component: EditQuestionPage },
  { path: '/profile', component: ProfilePage },
  {
    path: '/bookmarks',
    name: 'Bookmarks',
    component: () => import('../pages/BookmarkPage.vue')
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
