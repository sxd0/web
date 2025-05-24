<template>
  <div class="min-h-screen bg-black text-white w-full">
    <Header />
    <router-view />
  </div>
</template>

<script setup>
import Header from './components/Header.vue'
</script>
