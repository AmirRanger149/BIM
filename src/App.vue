<template>
  <div class="app" :class="{ 'dark-mode': isDark }">
    <Loader />
    <Navbar @toggle-theme="toggleTheme" :is-dark="isDark" />
    <Hero />
    <Gallery />
    <Statistics />
    <Articles />
    <Testimonials />
    <Certificates />
    <ContactForm />
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Loader from './components/Loader.vue'
import Navbar from './components/Navbar.vue'
import Hero from './components/Hero.vue'
import Gallery from './components/Gallery.vue'
import Statistics from './components/Statistics.vue'
import Articles from './components/Articles.vue'
import Testimonials from './components/Testimonials.vue'
import Certificates from './components/Certificates.vue'
import ContactForm from './components/ContactForm.vue'
import Footer from './components/Footer.vue'

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
</script>

<style>
.app {
  transition: background-color 0.3s ease;
}
</style>
