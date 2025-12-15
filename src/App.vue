<template>
  <div class="app" :class="{ 'dark-mode': isDark }">
    <Loader />
    <router-view />
    <ToastContainer />
  </div>
</template>

<script setup>
import { ref, onMounted, provide, watch } from 'vue'
import Loader from './components/Loader.vue'
import ToastContainer from './components/ToastContainer.vue'

const isDark = ref(false)

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDark.value = true
  }
})

const toggleTheme = () => {
  isDark.value = !isDark.value
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

// Watch for theme changes and update document class
watch(isDark, (newValue) => {
  if (newValue) {
    document.documentElement.classList.add('dark-mode')
  } else {
    document.documentElement.classList.remove('dark-mode')
  }
}, { immediate: true })

// Provide theme state and toggle function to all child components
provide('theme', {
  isDark,
  toggleTheme
})
</script>

<style>
.app {
  transition: background-color 0.3s ease;
}
</style>
