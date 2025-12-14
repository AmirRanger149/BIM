<template>
  <Transition name="fade">
    <div v-if="isLoading" class="loader-overlay">
      <div class="loader-container">
        <div class="loader-spinner">
          <div class="spinner-ring"></div>
          <div class="spinner-ring"></div>
          <div class="spinner-ring"></div>
        </div>
        <h2 class="loader-text">در حال بارگذاری...</h2>
        <div class="loader-progress">
          <div class="progress-bar" :style="{ width: progress + '%' }"></div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isLoading = ref(true)
const progress = ref(0)

onMounted(() => {
  // Simulate loading progress
  const interval = setInterval(() => {
    if (progress.value < 90) {
      progress.value += Math.random() * 15
    }
  }, 200)
  
  // Hide loader when page is fully loaded
  window.addEventListener('load', () => {
    progress.value = 100
    setTimeout(() => {
      isLoading.value = false
      clearInterval(interval)
    }, 500)
  })
  
  // Fallback: hide after 3 seconds
  setTimeout(() => {
    if (isLoading.value) {
      progress.value = 100
      setTimeout(() => {
        isLoading.value = false
        clearInterval(interval)
      }, 500)
    }
  }, 3000)
})
</script>

<style scoped>
.loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
}

.dark-mode .loader-overlay {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
}

.loader-container {
  text-align: center;
  max-width: 300px;
  width: 100%;
  padding: 2rem;
}

.loader-spinner {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 2rem;
}

.spinner-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 4px solid transparent;
  border-radius: 50%;
  animation: spin 1.5s cubic-bezier(0.5, 0, 0.5, 1) infinite;
}

.spinner-ring:nth-child(1) {
  border-top-color: rgba(255, 255, 255, 0.9);
  animation-delay: 0s;
}

.spinner-ring:nth-child(2) {
  border-top-color: rgba(255, 255, 255, 0.6);
  animation-delay: -0.5s;
  width: 85%;
  height: 85%;
  top: 7.5%;
  left: 7.5%;
}

.spinner-ring:nth-child(3) {
  border-top-color: rgba(255, 255, 255, 0.3);
  animation-delay: -1s;
  width: 70%;
  height: 70%;
  top: 15%;
  left: 15%;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loader-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin-bottom: 2rem;
  font-family: 'Vazirmatn', sans-serif;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.loader-progress {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: white;
  border-radius: 2px;
  transition: width 0.3s ease;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

.fade-enter-active {
  transition: opacity 0.3s ease;
}

.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .loader-spinner {
    width: 100px;
    height: 100px;
  }
  
  .loader-text {
    font-size: 1.2rem;
  }
}
</style>
