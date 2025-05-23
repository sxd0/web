<template>
  <div class="bg-gray-800 p-4 rounded-xl shadow mb-6">
    <h2 class="text-lg font-semibold mb-4">{{ title }}</h2>
    <slot />
  </div>
</template>

<script setup>
defineProps({
  title: String
})
</script>
