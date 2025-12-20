<template>
  <section id="certificates" class="certificates-section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">گواهینامه‌ها و استانداردها</h2>
        <p class="section-subtitle">مجوزها، گواهینامه‌ها و استانداردهای دریافتی</p>
      </div>
      
      <div class="certificates-grid">
        <router-link 
          v-for="cert in certificates" 
          :key="cert.id"
          :to="`/certificate/${cert.id}`"
          class="certificate-card"
        >
          <ImageSlider
            :image="cert.image"
            :images="cert.images"
            :icon="cert.icon"
            :gradient="cert.gradient"
            class="certificate-image"
          />
          <div class="certificate-info">
            <h3 class="certificate-title">{{ cert.title }}</h3>
            <p class="certificate-issuer">{{ cert.issuer }}</p>
            <p class="certificate-date">{{ cert.date }}</p>
            <div class="certificate-badge" :class="cert.type">
              {{ cert.type_label || cert.typeLabel }}
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCertificates, getSlider } from '../api/services'
import ImageSlider from './ImageSlider.vue'

const certificates = ref([])
const loading = ref(true)

const enrichCertificateWithSlider = async (cert) => {
  let images = []
  
  // Try to get slider images if slider_id is available
  if (cert.slider_id) {
    try {
      const response = await getSlider(cert.slider_id)
      const sliderData = response?.data || response
      if (sliderData?.images && Array.isArray(sliderData.images) && sliderData.images.length > 0) {
        images = sliderData.images
      }
    } catch (error) {
      console.warn(`Failed to fetch slider ${cert.slider_id}:`, error)
    }
  }
  
  // If no images from slider, use the image field
  if (images.length === 0 && cert.image) {
    images = [cert.image]
  }
  
  return {
    ...cert,
    images
  }
}

const fetchCertificates = async () => {
  try {
    loading.value = true
    const response = await getCertificates()
    const data = response.data || response
    const certList = Array.isArray(data) ? data : (data.data || [])
    
    if (certList && certList.length > 0) {
      // Enrich certificates with slider images
      const enrichedCerts = await Promise.all(
        certList.map(cert => enrichCertificateWithSlider(cert))
      )
      
      certificates.value = enrichedCerts
    } else {
      // Use mock data as fallback
      certificates.value = [
        {
          id: 1,
          title: 'ISO 9001:2015',
          issuer: 'سازمان بین‌المللی استاندارد',
          date: 'دی ۱۴۰۳',
          icon: '🏆',
          gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          type: 'international',
          type_label: 'بین‌المللی',
          description: 'گواهینامه مدیریت کیفیت ISO 9001:2015'
        },
        {
          id: 2,
          title: 'ISO 27001',
          issuer: 'سازمان بین‌المللی استاندارد',
          date: 'آذر ۱۴۰۳',
          icon: '🔐',
          gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
          type: 'security',
          type_label: 'امنیت'
        }
      ]
    }
  } catch (error) {
    console.error('خطا در دریافت گواهینامه‌ها:', error)
    // Set fallback certificates
    certificates.value = [
      {
        id: 1,
        title: 'ISO 9001:2015',
        issuer: 'سازمان بین‌المللی استاندارد',
        date: 'دی ۱۴۰۳',
        icon: '🏆',
        gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        type: 'international',
        type_label: 'بین‌المللی',
        description: 'گواهینامه مدیریت کیفیت ISO 9001:2015'
      }
    ]
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCertificates()
})
</script>

<style scoped>
.certificates-section {
  padding: 6rem 0;
  background: rgba(248, 249, 250, 0.5);
}

.dark-mode .certificates-section {
  background: rgba(45, 45, 45, 0.3);
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.dark-mode .section-title {
  color: #ffffff;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
}

.dark-mode .section-subtitle {
  color: #a0a0a0;
}

.certificates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.certificate-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
  cursor: pointer;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
}

.dark-mode .certificate-card {
  background: rgba(45, 45, 45, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
}

.certificate-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.dark-mode .certificate-card:hover {
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

.certificate-image {
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 20px 20px 0 0;
  overflow: hidden;
}

.certificate-icon {
  font-size: 4rem;
}

.certificate-info {
  padding: 2rem;
  flex: 1;
}

.certificate-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #1a1a1a;
}

.dark-mode .certificate-title {
  color: #ffffff;
}

.certificate-issuer {
  font-size: 1rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
}

.dark-mode .certificate-issuer {
  color: #a0a0a0;
}

.certificate-date {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 1rem;
}

.dark-mode .certificate-date {
  color: #a0a0a0;
}

.certificate-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 600;
}

.certificate-badge.international {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

.certificate-badge.security {
  background: rgba(240, 147, 251, 0.1);
  color: #f093fb;
}

.certificate-badge.certification {
  background: rgba(79, 172, 254, 0.1);
  color: #4facfe;
}

.certificate-badge.management {
  background: rgba(48, 207, 208, 0.1);
  color: #30cfd0;
}

@media (max-width: 768px) {
  .certificates-section {
    padding: 4rem 0;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .certificates-grid {
    grid-template-columns: 1fr;
  }
}
</style>
