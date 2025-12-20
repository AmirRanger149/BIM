<template>
  <div class="service-page" :class="{ 'dark-mode': isDark }">
    <Navbar @toggle-theme="toggleTheme" :is-dark="isDark" />
    
    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>در حال بارگیری خدمت...</p>
    </div>

    <!-- Error State -->
    <div v-if="error && !loading" class="error-container">
      <h2>خطا در بارگیری خدمت</h2>
      <p>{{ error }}</p>
      <router-link to="/" class="back-link">بازگشت به خانه</router-link>
    </div>

    <!-- Service Content -->
    <article v-if="service && !loading" 
             class="service-container"
             itemscope 
             itemtype="https://schema.org/Service">

      <!-- Breadcrumb -->
      <nav class="breadcrumb" itemscope itemtype="https://schema.org/BreadcrumbList">
        <div class="container">
          <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <router-link to="/" itemprop="item">
              <span itemprop="name">خانه</span>
            </router-link>
            <meta itemprop="position" content="1" />
          </span>
          <span class="separator">/</span>
          <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <span class="current" itemprop="name">{{ service.title }}</span>
            <meta itemprop="position" content="2" />
          </span>
        </div>
      </nav>

      <!-- Service Header -->
      <header class="service-header">
        <div class="container">
          <h1 class="service-title" itemprop="name">{{ service.title }}</h1>
          <p class="service-excerpt" itemprop="description">{{ service.description }}</p>
        </div>
      </header>

      <!-- Service Image/Gallery -->
      <section class="service-gallery">
        <div class="container">
          <ImageSlider
            v-if="service.images || service.image"
            :image="service.image"
            :images="service.images"
            :icon="service.icon"
            :gradient="service.gradient"
            class="service-main-image"
            itemprop="image"
          />
        </div>
      </section>

      <!-- Service Details -->
      <section class="service-details">
        <div class="container">
          <div class="details-grid">
            <!-- Main Content -->
            <div class="details-content">
              <h2>درباره خدمت</h2>
              <div class="service-text" itemprop="text">
                <p v-if="service.description">{{ service.description }}</p>
              </div>
              
              <!-- Features -->
              <div class="features" v-if="service.features && service.features.length">
                <h3>ویژگی‌های خدمت</h3>
                <ul class="features-list">
                  <li v-for="(feature, index) in service.features" :key="index">
                    <span class="feature-icon">✓</span>
                    <span>{{ feature }}</span>
                  </li>
                </ul>
              </div>
            </div>

            <!-- Sidebar -->
            <aside class="details-sidebar">
              <!-- Price -->
              <div class="price-box" v-if="service.price">
                <h3>قیمت</h3>
                <div class="price-value">{{ service.price }}</div>
              </div>

              <!-- Service Icon -->
              <div class="service-icon-box" v-if="service.icon">
                <div class="service-icon" :style="{ background: service.gradient || 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)' }">
                  {{ service.icon }}
                </div>
              </div>

              <!-- CTA Button -->
              <button class="cta-button" @click="scrollToContact">
                درخواست خدمت
                <span class="btn-arrow">→</span>
              </button>
            </aside>
          </div>
        </div>
      </section>
    </article>

    <!-- Contact Section CTA -->
    <section class="contact-cta">
      <div class="container">
        <h2>آماده برای شروع؟</h2>
        <p>با ما تماس بگیرید تا جزئیات بیشتر درباره این خدمت بدانید</p>
        <router-link to="/" class="contact-button">تماس با ما</router-link>
      </div>
    </section>

    <Footer v-if="!loading" />
  </div>
</template>

<script setup>
import { ref, inject, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getService, getSlider } from '../api/services'
import ImageSlider from '../components/ImageSlider.vue'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'

const route = useRoute()
const router = useRouter()
const { isDark, toggleTheme } = inject('theme')

const service = ref(null)
const loading = ref(true)
const error = ref(null)

const scrollToContact = () => {
  const contactSection = document.querySelector('.contact-cta')
  if (contactSection) {
    contactSection.scrollIntoView({ behavior: 'smooth' })
  }
}

// Fetch service data
const fetchService = async () => {
  try {
    loading.value = true
    error.value = null
    
    const serviceId = route.params.id
    
    // Fetch main service
    const response = await getService(serviceId)
    let serviceData = response.data || response
    
    // Enrich with slider images if available
    if (serviceData.slider_id) {
      try {
        const sliderResponse = await getSlider(serviceData.slider_id)
        const sliderData = sliderResponse?.data || sliderResponse
        if (sliderData?.images && Array.isArray(sliderData.images) && sliderData.images.length > 0) {
          serviceData.images = sliderData.images
        }
      } catch (sliderError) {
        console.warn('Failed to fetch slider images:', sliderError)
      }
    }
    
    service.value = serviceData
    updateMetaTags()
  } catch (err) {
    error.value = err.message || 'خطا در بارگیری خدمت'
    console.error('Error loading service:', err)
  } finally {
    loading.value = false
  }
}

const updateMetaTags = () => {
  if (!service.value) return
  
  const title = `${service.value.title} | مهندسین مشاور BIM`
  const description = service.value.description || 'خدمات حرفه‌ای'
  const image = service.value.image || '/default-og-image.png'
  
  document.title = title
  
  const metaTags = [
    { name: 'description', content: description },
    { property: 'og:title', content: title },
    { property: 'og:description', content: description },
    { property: 'og:image', content: image },
    { property: 'og:url', content: window.location.href },
    { property: 'og:type', content: 'website' },
    { name: 'twitter:card', content: 'summary_large_image' },
    { name: 'twitter:title', content: title },
    { name: 'twitter:description', content: description },
    { name: 'twitter:image', content: image }
  ]
  
  metaTags.forEach(tag => {
    const key = tag.name || tag.property
    const attr = tag.name ? 'name' : 'property'
    let element = document.querySelector(`meta[${attr}="${key}"]`)
    
    if (!element) {
      element = document.createElement('meta')
      element.setAttribute(attr, key)
      document.head.appendChild(element)
    }
    element.setAttribute('content', tag.content)
  })
  
  // Add canonical URL
  let canonical = document.querySelector('link[rel="canonical"]')
  if (!canonical) {
    canonical = document.createElement('link')
    canonical.setAttribute('rel', 'canonical')
    document.head.appendChild(canonical)
  }
  canonical.setAttribute('href', window.location.href)
}

onMounted(() => {
  fetchService()
})
</script>

<style scoped lang="css">
.service-page {
  background-color: #f9f9f9;
  transition: background-color 0.3s ease;
}

.service-page.dark-mode {
  background-color: #1a1a1a;
  color: #e0e0e0;
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 600px;
  text-align: center;
}

.error-container {
  color: #d32f2f;
}

.error-container h2 {
  margin-bottom: 1rem;
}

.back-link {
  display: inline-block;
  margin-top: 2rem;
  padding: 0.75rem 1.5rem;
  background-color: #0ea5e9;
  color: white;
  border-radius: 4px;
  text-decoration: none;
  transition: background-color 0.3s;
}

.back-link:hover {
  background-color: #06b6d4;
}

/* Breadcrumb */
.breadcrumb {
  background-color: #f5f5f5;
  padding: 1rem 0;
  font-size: 0.9rem;
}

.service-page.dark-mode .breadcrumb {
  background-color: #2a2a2a;
}

.breadcrumb .container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.breadcrumb a {
  color: #0ea5e9;
  text-decoration: none;
  transition: color 0.3s;
}

.breadcrumb a:hover {
  color: #06b6d4;
  text-decoration: underline;
}

.breadcrumb .separator {
  color: #999;
}

.breadcrumb .current {
  color: #666;
}

.service-page.dark-mode .breadcrumb .current {
  color: #bbb;
}

/* Service Header */
.service-header {
  padding: 4rem 0;
  text-align: center;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
}

.service-page.dark-mode .service-header {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
}

.service-title {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #333;
  font-weight: 700;
}

.service-page.dark-mode .service-title {
  color: #fff;
}

.service-excerpt {
  font-size: 1.1rem;
  color: #666;
  max-width: 600px;
  margin: 0 auto;
}

.service-page.dark-mode .service-excerpt {
  color: #bbb;
}

/* Service Gallery */
.service-gallery {
  padding: 3rem 0;
}

.service-main-image {
  width: 100%;
  height: 500px;
  object-fit: cover;
  border-radius: 8px;
}

/* Service Details */
.service-details {
  padding: 3rem 0;
}

.details-grid {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 3rem;
}

@media (max-width: 768px) {
  .details-grid {
    grid-template-columns: 1fr;
  }
}

.details-content h2,
.details-content h3 {
  font-size: 1.5rem;
  margin: 2rem 0 1rem 0;
  color: #333;
}

.service-page.dark-mode .details-content h2,
.service-page.dark-mode .details-content h3 {
  color: #fff;
}

.service-text {
  line-height: 1.8;
  color: #555;
  margin-bottom: 2rem;
}

.service-page.dark-mode .service-text {
  color: #ccc;
}

.service-text p {
  margin-bottom: 1rem;
}

/* Features List */
.features-list {
  list-style: none;
  padding: 0;
  margin: 1rem 0;
}

.features-list li {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid #eee;
}

.service-page.dark-mode .features-list li {
  border-bottom-color: #333;
}

.feature-icon {
  color: #0ea5e9;
  font-weight: bold;
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.features-list li span:last-child {
  color: #555;
}

.service-page.dark-mode .features-list li span:last-child {
  color: #ccc;
}

/* Sidebar */
.details-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.price-box,
.service-icon-box {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.service-page.dark-mode .price-box,
.service-page.dark-mode .service-icon-box {
  background-color: #2a2a2a;
}

.price-box h3,
.service-icon-box h3 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  color: #333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.service-page.dark-mode .price-box h3,
.service-page.dark-mode .service-icon-box h3 {
  color: #fff;
}

.price-value {
  font-size: 1.8rem;
  color: #0ea5e9;
  font-weight: bold;
}

.service-icon {
  width: 100%;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  border-radius: 8px;
}

.cta-button {
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: auto;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.btn-arrow {
  transition: transform 0.3s;
}

.cta-button:hover .btn-arrow {
  transform: translateX(4px);
}

/* Contact CTA Section */
.contact-cta {
  padding: 4rem 0;
  background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
  color: white;
  text-align: center;
}

.contact-cta h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.contact-cta p {
  font-size: 1.1rem;
  margin-bottom: 2rem;
  opacity: 0.95;
}

.contact-button {
  display: inline-block;
  padding: 1rem 2rem;
  background-color: white;
  color: #0ea5e9;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 600;
  transition: all 0.3s;
}

.contact-button:hover {
  background-color: #f5f5f5;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

/* Spinner */
.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #0ea5e9;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}
</style>
