<template>
  <section id="home" class="hero">
    <div class="hero-bg">
      <div v-if="sliderImages.length > 0" class="hero-slider">
        <div
          v-for="(img, idx) in sliderImages"
          :key="idx"
          class="slide"
          :class="{ active: idx === activeIndex }"
          :style="{ backgroundImage: `url(${img})` }"
        ></div>
        <div class="slider-overlay"></div>
        
        <!-- Progress Bar -->
        <div class="slider-progress">
          <div 
            v-for="(img, idx) in sliderImages" 
            :key="idx"
            class="progress-dot"
            :class="{ active: idx === activeIndex }"
            @click="setActiveSlide(idx)"
          ></div>
        </div>
      </div>
      <div v-else class="hero-orbs">
        <div class="gradient-orb orb-1"></div>
        <div class="gradient-orb orb-2"></div>
        <div class="gradient-orb orb-3"></div>
      </div>
    </div>
    
    <div class="container">
      <div class="hero-content">
        <div class="hero-badge">
          <span class="badge-dot"></span>
          اولین در ایران
        </div>
        
        <h1 class="hero-title">
          مهندسین مشاور
          <span class="gradient-text">دانش بنیان بیم</span>
          پیشرو در صنعت
        </h1>
        
        <p class="hero-subtitle">
          ارائه خدمات مهندسی، مشاوره و نظارت در پروژه‌های عمرانی
          <br />
          با بهره‌گیری از جدیدترین تکنولوژی‌های روز دنیا
        </p>
        
        <div class="hero-buttons">
          <button 
            v-if="featuredVideo"
            @click="openVideoModal"
            class="btn btn-secondary"
          >
            <span class="play-icon">▶</span>
            تماشای ویدیو
          </button>
        </div>
      </div>
    </div>
  </section>

  <!-- Video Modal -->
  <VideoModal 
    :is-open="showVideoModal" 
    :video="featuredVideo"
    @close="showVideoModal = false"
  />
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import VideoModal from './VideoModal.vue'
import { getSliders } from '../api/services'

const showVideoModal = ref(false)
const featuredVideo = ref(null)
const sliderImages = ref([])
const activeIndex = ref(0)
let rotateTimer = null

onMounted(async () => {
  // بارگذاری ویدیوی اول (اولویت دار)
  try {
    const response = await fetch('/api/videos?active_only=true&limit=1')
    if (response.ok) {
      const videos = await response.json()
      if (videos.length > 0) {
        featuredVideo.value = videos[0]
      }
    }
  } catch (error) {
    console.error('خطا در بارگذاری ویدیو:', error)
  }
})

onMounted(async () => {
  try {
    const res = await getSliders()
    const sliders = res?.data || []
    // find slider by name that contains 'hero' or 'header' (case-insensitive)
    const heroSlider = sliders.find(s => s.name && /hero|header|home/i.test(s.name))
    if (heroSlider && Array.isArray(heroSlider.images) && heroSlider.images.length > 0) {
      sliderImages.value = heroSlider.images
      // start rotation
      rotateTimer = setInterval(() => {
        activeIndex.value = (activeIndex.value + 1) % sliderImages.value.length
      }, 6000)
    }
  } catch (err) {
    console.error('خطا در بارگذاری اسلایدر هدر:', err)
  }
})

onBeforeUnmount(() => {
  if (rotateTimer) clearInterval(rotateTimer)
})

const openVideoModal = () => {
  showVideoModal.value = true
}

const setActiveSlide = (index) => {
  activeIndex.value = index
  // Reset timer
  if (rotateTimer) clearInterval(rotateTimer)
  rotateTimer = setInterval(() => {
    activeIndex.value = (activeIndex.value + 1) % sliderImages.value.length
  }, 6000)
}
</script>

<style scoped>
.hero {
  position: relative;
  padding: 8rem 0 6rem;
  overflow: hidden;
  min-height: 90vh;
  display: flex;
  align-items: center;
}

.hero-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.hero-slider { 
  position: absolute; 
  inset: 0; 
  display: block; 
  width: 100%;
  height: 100%;
}

.hero-slider .slide {
  position: absolute;
  inset: 0;
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  opacity: 0;
  transition: opacity 1.2s ease-in-out;
  animation: slideBackground 8s ease-in-out infinite;
}

.hero-slider .slide.active { 
  opacity: 1;
  animation: slideBackground 8s ease-in-out infinite;
}

.slider-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(0,0,0,0.35) 0%, rgba(102, 126, 234, 0.25) 100%);
  pointer-events: none;
  z-index: 1;
}

.slider-progress {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 0.5rem;
  z-index: 2;
}

.progress-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
}

.progress-dot:hover {
  background: rgba(255, 255, 255, 0.8);
  transform: scale(1.2);
}

.progress-dot.active {
  background: #0ea5e9;
  transform: scale(1.3);
}

.hero-orbs { 
  position: absolute; 
  inset: 0; 
  overflow: hidden;
  width: 100%;
  height: 100%;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(70px);
  opacity: 0.5;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
  top: -200px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
  bottom: -150px;
  left: -100px;
  animation-delay: 5s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: 10s;
}

@keyframes slideBackground {
  0% {
    transform: translateX(0) scale(1);
  }
  50% {
    transform: translateX(15px) scale(1.02);
  }
  100% {
    transform: translateX(0) scale(1);
  }
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -30px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
  position: relative;
  z-index: 2;
}

.hero-content {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
  font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 0.5rem 1.5rem;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 2rem;
  animation: fadeInDown 0.8s ease;
  backdrop-filter: blur(8px);
  font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.badge-dot {
  width: 8px;
  height: 8px;
  background: #4ade80;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.2);
  }
}

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 1.5rem;
  color: #fff;
  animation: fadeInUp 0.8s ease 0.2s both;
  font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  letter-spacing: -0.02em;
}

.gradient-text {
  background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
}

.hero-subtitle {
  font-size: 1.25rem;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.95);
  margin-bottom: 3rem;
  animation: fadeInUp 0.8s ease 0.4s both;
  font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-weight: 400;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 4rem;
  animation: fadeInUp 0.8s ease 0.6s both;
}

.btn {
  padding: 1rem 2rem;
  border: none;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.btn-primary {
  background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5);
}

.btn-primary .btn-arrow {
  transition: transform 0.3s ease;
}

.btn-primary:hover .btn-arrow {
  transform: translateX(-5px);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  border: 2px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(8px);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-3px);
}

.play-icon {
  font-size: 0.8rem;
}

.hero-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 3rem;
  max-width: 600px;
  margin: 0 auto;
  animation: fadeInUp 0.8s ease 0.8s both;
}

.stat {
  text-align: center;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.stat-label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .hero {
    padding: 4rem 0 3rem;
    min-height: auto;
  }
  
  .container {
    padding: 0 1.5rem;
  }
  
  .hero-badge {
    font-size: 0.85rem;
    padding: 0.4rem 1.2rem;
    margin-bottom: 1.5rem;
  }
  
  .hero-title {
    font-size: 2.2rem;
    line-height: 1.3;
  }
  
  .hero-subtitle {
    font-size: 1rem;
    margin-bottom: 2rem;
  }
  
  .hero-buttons {
    margin-bottom: 3rem;
  }
  
  .hero-stats {
    gap: 1.5rem;
    grid-template-columns: repeat(3, 1fr);
  }
  
  .stat-value {
    font-size: 1.8rem;
  }
  
  .stat-label {
    font-size: 0.8rem;
  }
  
  .gradient-orb {
    filter: blur(50px);
  }
  
  .orb-1 {
    width: 300px;
    height: 300px;
  }
  
  .orb-2 {
    width: 250px;
    height: 250px;
  }
  
  .orb-3 {
    width: 200px;
    height: 200px;
  }
}

@media (max-width: 480px) {
  .hero {
    padding: 3rem 0 2rem;
  }
  
  .hero-title {
    font-size: 1.8rem;
  }
  
  .hero-subtitle {
    font-size: 0.95rem;
    line-height: 1.6;
  }
  
  .btn {
    padding: 0.8rem 1.5rem;
    font-size: 0.95rem;
  }
  
  .hero-stats {
    gap: 1rem;
  }
  
  .stat-value {
    font-size: 1.5rem;
  }
  
  .stat-label {
    font-size: 0.75rem;
  }
}
</style>
