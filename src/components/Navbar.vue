<template>
  <nav class="navbar">
    <div class="container">
      <div class="nav-content">
        <router-link to="/" class="logo">
          <img v-if="logoUrl" :src="logoUrl" :alt="'Logo'" class="logo-image" />
          <span v-else class="logo-icon">🏗️</span>
        </router-link>
        
        <ul class="nav-links" :class="{ 'active': mobileMenuOpen }">
          <li><router-link to="/" class="nav-link" @click="handleNavClick('#home')">خانه</router-link></li>
          <li><a href="#" class="nav-link" @click.prevent="handleNavClick('#services')">خدمات</a></li>
          <li><router-link to="/media?tab=gallery" class="nav-link" @click="closeMobileMenu">گالری</router-link></li>
          <li><router-link to="/media?tab=articles" class="nav-link" @click="closeMobileMenu">مقالات</router-link></li>
          <li><a href="#" class="nav-link" @click.prevent="handleNavClick('#certificates')">گواهینامه‌ها</a></li>
          <li><router-link to="/contact" class="nav-link" @click="closeMobileMenu">تماس</router-link></li>
        </ul>

        <div class="nav-actions">
          <button @click="$emit('toggle-theme')" class="theme-toggle" aria-label="تغییر تم">
            <transition name="fade" mode="out-in">
              <span v-if="isDark" key="sun" class="theme-icon">☀</span>
              <span v-else key="moon" class="theme-icon">☽</span>
            </transition>
          </button>
          
          <button @click="toggleMobileMenu" class="mobile-menu-btn" aria-label="منوی موبایل">
            <span class="hamburger" :class="{ 'active': mobileMenuOpen }">
              <span></span>
              <span></span>
              <span></span>
            </span>
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useSiteSettings } from '../composables/useSiteSettings'

defineProps({
  isDark: Boolean
})

defineEmits(['toggle-theme'])

const router = useRouter()
const route = useRoute()
const mobileMenuOpen = ref(false)
const { logoUrl, loadSettings, addListener } = useSiteSettings()

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

const handleNavClick = (hash) => {
  closeMobileMenu()
  
  // اگر در صفحه اصلی نیستیم، اول به صفحه اصلی برویم
  if (route.path !== '/') {
    router.push('/').then(() => {
      setTimeout(() => {
        const element = document.querySelector(hash)
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'start' })
        }
      }, 100)
    })
  } else {
    // اگر در صفحه اصلی هستیم، مستقیم اسکرول کنیم
    const element = document.querySelector(hash)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }
}

onMounted(() => {
  loadSettings()
  addListener(() => {
    loadSettings()
  })
})

watch(() => route.path, () => {
  closeMobileMenu()
})
</script>

<style scoped>
.navbar {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 1000;
  transition: all 0.3s ease;
}

.dark-mode .navbar {
  background: rgba(26, 26, 26, 0.95);
  border-bottom-color: rgba(255, 255, 255, 0.1);
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 0;
  gap: 2rem;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.75rem;
  font-weight: 700;
  background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  cursor: pointer;
  transition: transform 0.3s ease;
  text-decoration: none;
  color: inherit;
  padding: 0.5rem 0;
}

.logo-image {
  height: 50px;
  width: auto;
  object-fit: contain;
  -webkit-background-clip: unset;
  -webkit-text-fill-color: unset;
  background-clip: unset;
  filter: drop-shadow(0 2px 4px rgba(14, 165, 233, 0.2));
}

.logo:hover {
  transform: scale(1.05);
}

.logo-icon {
  font-size: 1.8rem;
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 2.5rem;
  margin: 0;
  padding: 0;
}

.nav-link {
  color: #1a1a1a;
  text-decoration: none;
  font-weight: 500;
  font-size: 1rem;
  position: relative;
  transition: color 0.3s ease;
}

.dark-mode .nav-link {
  color: #ffffff;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
  transition: width 0.3s ease;
}

.nav-link:hover::after {
  width: 100%;
}

.nav-link:hover {
  color: #0ea5e9;
}

.theme-toggle {
  background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 50px;
  cursor: pointer;
  font-size: 1.3rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
}

.theme-toggle:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 6px 20px rgba(14, 165, 233, 0.4);
}

.theme-icon {
  display: block;
}

.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.hamburger {
  width: 25px;
  height: 20px;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.hamburger span {
  display: block;
  height: 3px;
  background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
  border-radius: 3px;
  transition: all 0.3s ease;
}

.hamburger.active span:nth-child(1) {
  transform: translateY(8.5px) rotate(45deg);
}

.hamburger.active span:nth-child(2) {
  opacity: 0;
}

.hamburger.active span:nth-child(3) {
  transform: translateY(-8.5px) rotate(-45deg);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .mobile-menu-btn {
    display: block;
  }
  .nav-links {
    gap: 1.5rem;
  }
  
  .nav-link {
    font-size: 0.9rem;
  }
}

@media (max-width: 640px) {
  .container {
    padding: 0 1rem;
  }
  
  .nav-links {
    position: fixed;
    top: 73px;
    right: -100%;
    width: 100%;
    height: calc(100vh - 73px);
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(10px);
    flex-direction: column;
    justify-content: flex-start;
    padding: 2rem;
    gap: 2rem;
    transition: right 0.3s ease;
    box-shadow: -5px 0 15px rgba(0, 0, 0, 0.1);
  }
  
  .dark-mode .nav-links {
    background: rgba(26, 26, 26, 0.98);
  }
  
  .nav-links.active {
    right: 0;
  }
  
  .nav-link {
    font-size: 1.2rem;
    padding: 1rem;
    width: 100%;
    text-align: center;
    border-radius: 10px;
    transition: all 0.3s ease;
  }
  
  .nav-link:hover {
    background: rgba(102, 126, 234, 0.1);
  }
}
</style>
