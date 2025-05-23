<template>
  <div class="min-h-screen bg-gray-900 text-white">
    <Header />
    <router-view />
  </div>
</template>

<script setup>
import Header from './components/Header.vue'
</script>
