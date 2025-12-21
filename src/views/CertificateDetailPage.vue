<template>
  <div class="certificate-page" :class="{ 'dark-mode': isDark }">
    <Navbar @toggle-theme="toggleTheme" :is-dark="isDark" />
    
    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>در حال بارگیری گواهینامه...</p>
    </div>

    <!-- Error State -->
    <div v-if="error && !loading" class="error-container">
      <h2>خطا در بارگیری گواهینامه</h2>
      <p>{{ error }}</p>
      <router-link to="/" class="back-link">بازگشت به خانه</router-link>
    </div>

    <!-- Certificate Content -->
    <article v-if="certificate && !loading" class="certificate-container">

      <!-- Breadcrumb -->
      <nav class="breadcrumb">
        <div class="container">
          <span>
            <router-link to="/">خانه</router-link>
          </span>
          <span class="separator">/</span>
          <span>
            <span class="current">{{ certificate.title }}</span>
          </span>
        </div>
      </nav>

      <!-- Certificate Header -->
      <header class="certificate-header">
        <div class="container">
          <div class="certificate-badge" :class="certificate.type">
            {{ certificate.type_label || certificate.typeLabel }}
          </div>
          <h1 class="certificate-title">{{ certificate.title }}</h1>
          <p class="certificate-issuer">صادر کننده: {{ certificate.issuer }}</p>
          <p class="certificate-date">تاریخ صدور: {{ certificate.date }}</p>
        </div>
      </header>

      <!-- Certificate Image/Gallery -->
      <section class="certificate-gallery">
        <div class="container">
          <ImageSlider
            v-if="certificate.images || certificate.image"
            :image="certificate.image"
            :images="certificate.images"
            :icon="certificate.icon"
            :gradient="certificate.gradient"
            class="certificate-main-image"
          />
        </div>
      </section>

      <!-- Certificate Details -->
      <section class="certificate-details">
        <div class="container">
          <div class="details-grid">
            <!-- Main Content -->
            <div class="details-content">
              <h2>درباره این گواهینامه</h2>
              
              <div class="certificate-description">
                <p v-if="certificate.description">{{ certificate.description }}</p>
                <p v-else>این گواهینامه نشان‌دهنده کیفیت و استانداردهای بین‌المللی است که سازمان ما مطابق آن عمل می‌کند.</p>
              </div>

              <!-- Certificate Details -->
              <div class="certificate-specs">
                <div class="spec-item">
                  <span class="spec-label">شماره گواهی:</span>
                  <span class="spec-value">{{ certificate.cert_number || certificate.certNumber || 'نامشخص' }}</span>
                </div>
                <div class="spec-item">
                  <span class="spec-label">تاریخ صدور:</span>
                  <span class="spec-value">{{ certificate.date }}</span>
                </div>
                <div class="spec-item" v-if="certificate.validity || certificate.expiry_date">
                  <span class="spec-label">تاریخ انقضا:</span>
                  <span class="spec-value">{{ certificate.validity || certificate.expiry_date }}</span>
                </div>
                <div class="spec-item">
                  <span class="spec-label">نوع:</span>
                  <span class="spec-value">{{ certificate.type_label || certificate.typeLabel }}</span>
                </div>
              </div>
            </div>

            <!-- Sidebar -->
            <aside class="details-sidebar">
              <!-- Certificate Type Badge -->
              <div class="certificate-type-box">
                <div 
                  class="type-badge-large" 
                  :class="certificate.type"
                  :style="{ background: certificate.gradient || getGradientByType(certificate.type) }"
                >
                  {{ certificate.icon || '📜' }}
                </div>
                <h3>{{ certificate.type_label || certificate.typeLabel }}</h3>
              </div>

              <!-- Verification Box -->
              <div class="verification-box">
                <h3>التزام ما</h3>
                <p>این گواهینامه نشان‌دهنده تعهد ما به حفظ بالاترین استانداردهای کیفی و ایمنی در تمام پروژه‌های خود است.</p>
              </div>

              <!-- Download Certificate -->
              <button class="download-button" @click="downloadCertificate">
                دانلود گواهینامه
                <span class="btn-icon">⬇</span>
              </button>
            </aside>
          </div>
        </div>
      </section>

      <!-- Additional Info -->
      <section class="additional-info" v-if="certificate.additional_info">
        <div class="container">
          <h2>اطلاعات تکمیلی</h2>
          <p>{{ certificate.additional_info }}</p>
        </div>
      </section>
    </article>

    <Footer v-if="!loading" />
  </div>
</template>

<script setup>
import { ref, inject, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getCertificate, getSlider } from '../api/services'
import ImageSlider from '../components/ImageSlider.vue'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'

const route = useRoute()
const { isDark, toggleTheme } = inject('theme')

const certificate = ref(null)
const loading = ref(true)
const error = ref(null)

const getGradientByType = (type) => {
  const gradients = {
    'international': 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)',
    'national': 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)',
    'standard': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'certificate': 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
  }
  return gradients[type] || 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)'
}

const downloadCertificate = () => {
  if (certificate.value?.image) {
    const link = document.createElement('a')
    link.href = certificate.value.image
    link.download = `${certificate.value.title}.pdf`
    link.click()
  }
}

// Fetch certificate data
const fetchCertificate = async () => {
  try {
    loading.value = true
    error.value = null
    
    const certificateId = route.params.id
    
    // Fetch main certificate
    const response = await getCertificate(certificateId)
    let certificateData = response.data || response
    
    // Enrich with slider images if available
    if (certificateData.slider_id) {
      try {
        const sliderResponse = await getSlider(certificateData.slider_id)
        const sliderData = sliderResponse?.data || sliderResponse
        if (sliderData?.images && Array.isArray(sliderData.images) && sliderData.images.length > 0) {
          certificateData.images = sliderData.images
        }
      } catch (sliderError) {
        console.warn('Failed to fetch slider images:', sliderError)
      }
    }
    
    certificate.value = certificateData
    updateMetaTags()
  } catch (err) {
    error.value = err.message || 'خطا در بارگیری گواهینامه'
    console.error('Error loading certificate:', err)
  } finally {
    loading.value = false
  }
}

const updateMetaTags = () => {
  if (!certificate.value) return
  
  const title = `${certificate.value.title} | مهندسین مشاور BIM`
  const description = certificate.value.description || 'گواهینامه و استاندارد'
  const image = certificate.value.image || '/default-og-image.png'
  
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
}

onMounted(() => {
  fetchCertificate()
})
</script>

<style scoped lang="css">
.certificate-page {
  background-color: #f9f9f9;
  transition: background-color 0.3s ease;
}

.certificate-page.dark-mode {
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

.certificate-page.dark-mode .breadcrumb {
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

.certificate-page.dark-mode .breadcrumb .current {
  color: #bbb;
}

/* Certificate Header */
.certificate-header {
  padding: 4rem 0;
  text-align: center;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
}

.certificate-page.dark-mode .certificate-header {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
}

.certificate-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #0ea5e9;
  color: white;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 1rem;
  text-transform: capitalize;
}

.certificate-badge.national {
  background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
}

.certificate-badge.standard {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.certificate-title {
  font-size: 2.5rem;
  margin: 1rem 0 0.5rem 0;
  color: #333;
  font-weight: 700;
}

.certificate-page.dark-mode .certificate-title {
  color: #fff;
}

.certificate-issuer,
.certificate-date {
  font-size: 1rem;
  color: #666;
  margin: 0.25rem 0;
}

.certificate-page.dark-mode .certificate-issuer,
.certificate-page.dark-mode .certificate-date {
  color: #aaa;
}

/* Certificate Gallery */
.certificate-gallery {
  padding: 3rem 0;
}

.certificate-main-image {
  width: 100%;
  height: 500px;
  object-fit: cover;
  border-radius: 8px;
}

/* Certificate Details */
.certificate-details {
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

.certificate-page.dark-mode .details-content h2,
.certificate-page.dark-mode .details-content h3 {
  color: #fff;
}

.certificate-description {
  line-height: 1.8;
  color: #555;
  margin-bottom: 2rem;
}

.certificate-page.dark-mode .certificate-description {
  color: #ccc;
}

.certificate-description p {
  margin-bottom: 1rem;
}

/* Specs */
.certificate-specs {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin: 2rem 0;
  padding: 2rem;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.certificate-page.dark-mode .certificate-specs {
  background-color: #2a2a2a;
}

.spec-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 1px solid #ddd;
}

.certificate-page.dark-mode .spec-item {
  border-bottom-color: #444;
}

.spec-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.spec-label {
  font-weight: 600;
  color: #333;
}

.certificate-page.dark-mode .spec-label {
  color: #fff;
}

.spec-value {
  color: #0ea5e9;
  font-weight: 500;
}

/* Sidebar */
.details-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.certificate-type-box {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.certificate-page.dark-mode .certificate-type-box {
  background-color: #2a2a2a;
}

.type-badge-large {
  width: 100%;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.certificate-type-box h3 {
  margin: 0;
  font-size: 1rem;
  color: #333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.certificate-page.dark-mode .certificate-type-box h3 {
  color: #fff;
}

.verification-box {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-right: 4px solid #0ea5e9;
}

.certificate-page.dark-mode .verification-box {
  background-color: #2a2a2a;
}

.verification-box h3 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  color: #333;
}

.certificate-page.dark-mode .verification-box h3 {
  color: #fff;
}

.verification-box p {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
  line-height: 1.6;
}

.certificate-page.dark-mode .verification-box p {
  color: #aaa;
}

.download-button {
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
}

.download-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

/* Additional Info */
.additional-info {
  padding: 3rem 0;
  background-color: white;
  margin-top: 2rem;
}

.certificate-page.dark-mode .additional-info {
  background-color: #2a2a2a;
}

.additional-info h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
}

.certificate-page.dark-mode .additional-info h2 {
  color: #fff;
}

.additional-info p {
  line-height: 1.8;
  color: #555;
}

.certificate-page.dark-mode .additional-info p {
  color: #ccc;
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
