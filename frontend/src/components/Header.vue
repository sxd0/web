<template>
  <header class="bg-gray-800 p-4 shadow">
    <div class="container mx-auto flex justify-between items-center">
      <h1 class="text-xl font-bold">QuestFlow</h1>
      <nav class="flex gap-4 text-gray-300">
        <RouterLink to="/" class="hover:text-white">Главная</RouterLink>
        <RouterLink to="/create" class="hover:text-white">Создать</RouterLink>
        <RouterLink to="/profile" class="hover:text-white">Профиль</RouterLink>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>
