<template>
  <div class="min-h-screen bg-black text-white w-full">
    <header class="bg-gray-900 p-4 shadow mb-6">
      <nav class="container mx-auto flex justify-between items-center">
        <h1 class="text-xl font-bold text-green-400">QuestFlow</h1>
        <div class="space-x-4">
          <router-link to="/" class="hover:text-green-400">Главная</router-link>
          <router-link to="/create" class="hover:text-green-400">Создать</router-link>
          <router-link to="/profile" class="hover:text-green-400">Профиль</router-link>
        </div>
      </nav>
    </header>

    <router-view />
  </div>
</template>

<style>
body {
  margin: 0;
  font-family: 'Segoe UI', sans-serif;
}
</style>
