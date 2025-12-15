<template>
  <section id="certificates" class="certificates-section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">گواهینامه‌ها و استانداردها</h2>
        <p class="section-subtitle">مجوزها، گواهینامه‌ها و استانداردهای دریافتی</p>
      </div>
      
      <div class="certificates-grid">
        <div 
          v-for="cert in certificates" 
          :key="cert.id"
          class="certificate-card"
          @click="openCertificate(cert)"
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
              {{ cert.typeLabel }}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Certificate Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="selectedCert" class="cert-modal-overlay" @click="closeCertificate">
          <div class="cert-modal-content" @click.stop>
            <button class="modal-close" @click="closeCertificate">✕</button>
            
            <ImageSlider
              :image="selectedCert.image"
              :images="selectedCert.images"
              :icon="selectedCert.icon"
              :gradient="selectedCert.gradient"
              class="cert-modal-image"
            />
            
            <div class="cert-modal-body">
              <div class="cert-badge-large" :class="selectedCert.type">
                {{ selectedCert.typeLabel }}
              </div>
              <h2 class="cert-modal-title">{{ selectedCert.title }}</h2>
              <p class="cert-modal-issuer">{{ selectedCert.issuer }}</p>
              <p class="cert-modal-date">صادر شده در: {{ selectedCert.date }}</p>
              <p class="cert-modal-description">{{ selectedCert.description }}</p>
              
              <div class="cert-details">
                <div class="cert-detail-item">
                  <span class="detail-label">شماره گواهی:</span>
                  <span class="detail-value">{{ selectedCert.certNumber }}</span>
                </div>
                <div class="cert-detail-item">
                  <span class="detail-label">اعتبار:</span>
                  <span class="detail-value">{{ selectedCert.validity }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCertificates, getSlider } from '../api/services'
import ImageSlider from './ImageSlider.vue'

const certificates = ref([
  {
    id: 1,
    title: 'ISO 9001:2015',
    issuer: 'سازمان بین‌المللی استاندارد',
    date: 'دی ۱۴۰۳',
    icon: '🏆',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    type: 'international',
    typeLabel: 'بین‌المللی',
    description: 'گواهینامه مدیریت کیفیت ISO 9001:2015 که نشان‌دهنده تعهد ما به ارائه خدمات با کیفیت و بهبود مستمر فرآیندها است.',
    certNumber: 'ISO-9001-2023-1234',
    validity: 'تا دی ۱۴۰۶'
  },
  {
    id: 2,
    title: 'ISO 27001',
    issuer: 'سازمان بین‌المللی استاندارد',
    date: 'آذر ۱۴۰۳',
    icon: '🔐',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    type: 'security',
    typeLabel: 'امنیت',
    description: 'گواهینامه مدیریت امنیت اطلاعات که تضمین می‌کند داده‌های شما با بالاترین استانداردهای امنیتی محافظت می‌شوند.',
    certNumber: 'ISO-27001-2023-5678',
    validity: 'تا آذر ۱۴۰۶'
  },
  {
    id: 3,
    title: 'Microsoft Certified',
    issuer: 'Microsoft Corporation',
    date: 'آبان ۱۴۰۳',
    icon: '🎓',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    type: 'certification',
    typeLabel: 'گواهینامه تخصصی',
    description: 'گواهینامه تخصصی Microsoft Azure و .NET که نشان‌دهنده تخصص تیم ما در تکنولوژی‌های Microsoft است.',
    certNumber: 'MS-AZ-900-2023',
    validity: 'مادام‌العمر'
  },
  {
    id: 4,
    title: 'AWS Certified',
    issuer: 'Amazon Web Services',
    date: 'مهر ۱۴۰۳',
    icon: '☁️',
    gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    type: 'certification',
    typeLabel: 'گواهینامه تخصصی',
    description: 'گواهینامه Solutions Architect از AWS که نشان‌دهنده توانایی طراحی و پیاده‌سازی سیستم‌های مقیاس‌پذیر در فضای ابری است.',
    certNumber: 'AWS-SAA-C03-2023',
    validity: 'تا مهر ۱۴۰۶'
  },
  {
    id: 5,
    title: 'Google Cloud Certified',
    issuer: 'Google Cloud',
    date: 'شهریور ۱۴۰۳',
    icon: '🌐',
    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    type: 'certification',
    typeLabel: 'گواهینامه تخصصی',
    description: 'گواهینامه Professional Cloud Architect که تخصص ما در طراحی زیرساخت‌های ابری Google را تایید می‌کند.',
    certNumber: 'GCP-PCA-2023',
    validity: 'تا شهریور ۱۴۰۵'
  },
  {
    id: 6,
    title: 'Scrum Master Certified',
    issuer: 'Scrum Alliance',
    date: 'مرداد ۱۴۰۳',
    icon: '📋',
    gradient: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
    type: 'management',
    typeLabel: 'مدیریت پروژه',
    description: 'گواهینامه Certified ScrumMaster که نشان‌دهنده تسلط تیم ما بر متدولوژی Agile و مدیریت پروژه است.',
    certNumber: 'CSM-2023-9876',
    validity: 'تا مرداد ۱۴۰۵'
  }
])

const selectedCert = ref(null)
const loading = ref(true)

const openCertificate = (cert) => {
  selectedCert.value = cert
  document.body.style.overflow = 'hidden'
}

const closeCertificate = () => {
  selectedCert.value = null
  document.body.style.overflow = ''
}

// افزودن تصاویر اسلایدر به گواهینامه
const enrichCertificateWithSlider = async (cert) => {
  // اگر slider_id موجود بود، تصاویر slider را دریافت کن
  if (cert.slider_id) {
    try {
      const sliderResponse = await getSlider(cert.slider_id)
      if (sliderResponse.data && sliderResponse.data.images) {
        return {
          ...cert,
          images: sliderResponse.data.images
        }
      }
    } catch (err) {
      console.error('Error loading slider:', err)
    }
  }
  // اگر image موجود بود اما slider نبود، آن را به عنوان images نیز اضافه کن
  if (cert.image && !cert.images) {
    return {
      ...cert,
      images: [cert.image]
    }
  }
  return cert
}

// Fetch certificates from API
const fetchCertificates = async () => {
  try {
    loading.value = true
    const response = await getCertificates()
    let apiCerts = response.data || []
    
    if (apiCerts.length > 0) {
      // Map API data to certificates format
      let mappedCerts = apiCerts.map((cert) => ({
        id: cert.id,
        title: cert.title || 'گواهینامه',
        issuer: cert.issuer || 'سازمان',
        date: cert.date || '',
        icon: cert.icon || '🏆',
        gradient: cert.gradient || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        type: cert.type || 'standard',
        typeLabel: cert.type_label || 'گواهینامه',
        description: cert.description || '',
        certNumber: `CERT-${cert.id}`,
        validity: '۳ سال',
        slider_id: cert.slider_id
      }))
      
      // افزودن تصاویر اسلایدر
      mappedCerts = await Promise.all(mappedCerts.map(cert => enrichCertificateWithSlider(cert)))
      
      certificates.value = mappedCerts
    }
  } catch (err) {
    console.error('Error fetching certificates:', err)
    // Keep default certificates as fallback
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

/* Modal */
.cert-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 2rem;
  overflow-y: auto;
}

.cert-modal-content {
  background: white;
  border-radius: 25px;
  max-width: 1000px;
  width: 95%;
  max-height: 95vh;
  position: relative;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  overflow-y: auto;
}

.dark-mode .cert-modal-content {
  background: #2d2d2d;
}

.modal-close {
  position: absolute;
  top: 1.5rem;
  left: 1.5rem;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  color: #1a1a1a;
  z-index: 10;
}

.dark-mode .modal-close {
  background: rgba(0, 0, 0, 0.5);
  color: #ffffff;
}

.modal-close:hover {
  background: rgba(255, 0, 0, 0.1);
  color: #ff0000;
  transform: scale(1.1);
}

.cert-modal-image {
  height: 60vh;
  max-height: 700px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  overflow: hidden;
}

.cert-modal-body {
  padding: 3rem;
}

.cert-badge-large {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

.cert-badge-large.international {
  background: rgba(102, 126, 234, 0.15);
  color: #667eea;
}

.cert-badge-large.security {
  background: rgba(240, 147, 251, 0.15);
  color: #f093fb;
}

.cert-badge-large.certification {
  background: rgba(79, 172, 254, 0.15);
  color: #4facfe;
}

.cert-badge-large.management {
  background: rgba(48, 207, 208, 0.15);
  color: #30cfd0;
}

.cert-modal-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.dark-mode .cert-modal-title {
  color: #ffffff;
}

.cert-modal-issuer {
  font-size: 1.2rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.dark-mode .cert-modal-issuer {
  color: #a0a0a0;
}

.cert-modal-date {
  font-size: 1rem;
  color: #6c757d;
  margin-bottom: 2rem;
}

.dark-mode .cert-modal-date {
  color: #a0a0a0;
}

.cert-modal-description {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #1a1a1a;
  margin-bottom: 2rem;
}

.dark-mode .cert-modal-description {
  color: #ffffff;
}

.cert-details {
  background: rgba(102, 126, 234, 0.05);
  padding: 1.5rem;
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.dark-mode .cert-details {
  background: rgba(102, 126, 234, 0.1);
}

.cert-detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-label {
  font-weight: 600;
  color: #6c757d;
}

.dark-mode .detail-label {
  color: #a0a0a0;
}

.detail-value {
  font-weight: 700;
  color: #667eea;
}

.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .cert-modal-content,
.modal-leave-to .cert-modal-content {
  transform: scale(0.9);
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
  
  .cert-modal-content {
    margin: 1rem;
  }
  
  .cert-modal-body {
    padding: 2rem;
  }
  
  .cert-modal-title {
    font-size: 1.8rem;
  }
  
  .cert-modal-icon {
    font-size: 4rem;
  }
}
</style>
