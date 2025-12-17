<template>
  <div class="admin-settings admin-page">
    <div class="admin-section-header">
      <div>
        <div class="eyebrow">⚙️ تنظیمات</div>
        <h2>تنظیمات عمومی سایت</h2>
        <p class="muted">مدیریت لوگو، نام سایت و سایر تنظیمات عمومی</p>
      </div>
    </div>

    <div class="settings-grid">
      <!-- لوگو -->
      <div class="settings-card glass-card">
        <div class="card-header">
          <h3>🎨 لوگوی برنامه</h3>
          <p>تصویر لوگوی نمایش‌داده‌شده در هدر سایت</p>
        </div>
        
        <div class="setting-content">
          <div v-if="logoUrl" class="logo-preview">
            <img :src="logoUrl" :alt="'Logo'" class="logo-image" />
            <button @click="removeLogo" class="btn-remove-image">✕</button>
          </div>
          <div v-else class="no-logo">
            <p>هنوز لوگویی تعیین نشده</p>
          </div>

          <div class="upload-section">
            <div class="file-input-wrapper">
              <input
                type="file"
                @change="handleLogoUpload"
                accept="image/*"
                class="file-input"
              />
              <span class="upload-label">📁 انتخاب لوگو</span>
            </div>
            <div class="url-input">
              <input 
                v-model="newLogoUrl" 
                type="url" 
                placeholder="یا URL لوگو را پیوند کنید"
                class="url-input-field"
              />
              <button @click="setLogoUrl" class="btn-small">تنظیم</button>
            </div>
            <div v-if="uploadingLogo" class="uploading-status">درحال آپلود...</div>
          </div>
        </div>

        <div class="card-actions">
          <button v-if="logoUrl" @click="saveLogo" class="btn-primary">
            💾 ذخیره لوگو
          </button>
          <span v-else class="text-muted">لطفاً لوگویی انتخاب کنید</span>
        </div>
      </div>

      <!-- نام سایت -->
      <div class="settings-card glass-card">
        <div class="card-header">
          <h3>📛 نام سایت</h3>
          <p>نام نمایش‌داده‌شده در عنوان صفحات</p>
        </div>
        
        <div class="setting-content">
          <input 
            v-model="siteName" 
            type="text" 
            placeholder="نام سایت را وارد کنید"
            class="form-input"
          />
        </div>

        <div class="card-actions">
          <button @click="saveSiteName" class="btn-primary">
            💾 ذخیره نام
          </button>
        </div>
      </div>

      <!-- توضیح سایت -->
      <div class="settings-card glass-card">
        <div class="card-header">
          <h3>📝 توضیح سایت</h3>
          <p>متای توضیح برای موتورهای جستجو</p>
        </div>
        
        <div class="setting-content">
          <textarea 
            v-model="siteDescription" 
            placeholder="توضیح سایت را وارد کنید"
            class="form-textarea"
            rows="4"
          ></textarea>
        </div>

        <div class="card-actions">
          <button @click="saveSiteDescription" class="btn-primary">
            💾 ذخیره توضیح
          </button>
        </div>
      </div>

      <!-- Favicon -->
      <div class="settings-card glass-card">
        <div class="card-header">
          <h3>🖼️ نماد سایت (Favicon)</h3>
          <p>آیکون نمایش‌داده‌شده در تب مرورگر</p>
        </div>
        
        <div class="setting-content">
          <div v-if="faviconUrl" class="favicon-preview">
            <img :src="faviconUrl" :alt="'Favicon'" class="favicon-image" />
            <button @click="removeFavicon" class="btn-remove-image">✕</button>
          </div>
          <div v-else class="no-favicon">
            <p>هنوز faviconی تعیین نشده</p>
          </div>

          <div class="upload-section">
            <div class="file-input-wrapper">
              <input
                type="file"
                @change="handleFaviconUpload"
                accept="image/*"
                class="file-input"
              />
              <span class="upload-label">📁 انتخاب Favicon</span>
            </div>
            <div class="url-input">
              <input 
                v-model="newFaviconUrl" 
                type="url" 
                placeholder="یا URL favicon را پیوند کنید"
                class="url-input-field"
              />
              <button @click="setFaviconUrl" class="btn-small">تنظیم</button>
            </div>
            <div v-if="uploadingFavicon" class="uploading-status">درحال آپلود...</div>
          </div>
        </div>

        <div class="card-actions">
          <button v-if="faviconUrl" @click="saveFavicon" class="btn-primary">
            💾 ذخیره Favicon
          </button>
          <span v-else class="text-muted">لطفاً faviconی انتخاب کنید</span>
        </div>
      </div>
    </div>

    <!-- اسلایدر صفحه اصلی -->
    <div class="sliders-section">
      <div class="section-header-local">
        <h2>🎬 اسلایدرهای صفحه اصلی</h2>
        <p>مدیریت تصاویری که در قسمت Hero (هدر) صفحه اصلی نمایش می‌یابند</p>
      </div>

      <div class="info-box">
        <p>برای مدیریت اسلایدرهای صفحه اصلی، لطفاً به صفحه مخصوص Hero Sliders برو</p>
        <router-link to="/admin/hero-sliders" class="btn-primary">
          🎬 مدیریت Hero Sliders
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { adminService } from '../api/services'
import { success, error } from '../composables/useToast'

const router = useRouter()

// لوگو
const logoUrl = ref('')
const newLogoUrl = ref('')
const uploadingLogo = ref(false)
const savedLogo = ref('')

// Favicon
const faviconUrl = ref('')
const newFaviconUrl = ref('')
const uploadingFavicon = ref(false)
const savedFavicon = ref('')

// سایت
const siteName = ref('')
const siteDescription = ref('')

// اسلایدرها
const heroSliders = ref([])
const loadingSliders = ref(false)

const loadSettings = async () => {
  try {
    const settings = await adminService.getSettings()
    
    // پر کردن تنظیمات
    const logoSetting = settings.find(s => s.key === 'logo')
    if (logoSetting && logoSetting.value) {
      logoUrl.value = logoSetting.value
      savedLogo.value = logoSetting.value
    }

    const faviconSetting = settings.find(s => s.key === 'favicon')
    if (faviconSetting && faviconSetting.value) {
      faviconUrl.value = faviconSetting.value
      savedFavicon.value = faviconSetting.value
    }

    const siteName_setting = settings.find(s => s.key === 'site_name')
    if (siteName_setting && siteName_setting.value) {
      siteName.value = siteName_setting.value
    }

    const description_setting = settings.find(s => s.key === 'site_description')
    if (description_setting && description_setting.value) {
      siteDescription.value = description_setting.value
    }
  } catch (err) {
    console.error('خطا در بارگذاری تنظیمات:', err)
  }
}

const handleLogoUpload = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  uploadingLogo.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    const response = await adminService.uploadFile(formData)
    logoUrl.value = response.url
    success('تصویر لوگو آپلود شد')
  } catch (err) {
    error('خطا در آپلود تصویر')
  } finally {
    uploadingLogo.value = false
  }
}

const handleFaviconUpload = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  uploadingFavicon.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    const response = await adminService.uploadFile(formData)
    faviconUrl.value = response.url
    success('تصویر favicon آپلود شد')
  } catch (err) {
    error('خطا در آپلود تصویر')
  } finally {
    uploadingFavicon.value = false
  }
}

const setLogoUrl = () => {
  if (newLogoUrl.value.trim()) {
    logoUrl.value = newLogoUrl.value.trim()
    newLogoUrl.value = ''
    success('لوگو تنظیم شد')
  }
}

const setFaviconUrl = () => {
  if (newFaviconUrl.value.trim()) {
    faviconUrl.value = newFaviconUrl.value.trim()
    newFaviconUrl.value = ''
    success('Favicon تنظیم شد')
  }
}

const removeLogo = () => {
  logoUrl.value = ''
}

const removeFavicon = () => {
  faviconUrl.value = ''
}

const saveLogo = async () => {
  try {
    await adminService.updateSetting('logo', logoUrl.value)
    savedLogo.value = logoUrl.value
    success('لوگو با موفقیت ذخیره شد')
  } catch (err) {
    error('خطا در ذخیره لوگو')
  }
}

const saveFavicon = async () => {
  try {
    await adminService.updateSetting('favicon', faviconUrl.value)
    savedFavicon.value = faviconUrl.value
    success('Favicon با موفقیت ذخیره شد')
  } catch (err) {
    error('خطا در ذخیره favicon')
  }
}

const saveSiteName = async () => {
  try {
    await adminService.updateSetting('site_name', siteName.value)
    success('نام سایت با موفقیت ذخیره شد')
  } catch (err) {
    error('خطا در ذخیره نام سایت')
  }
}

const saveSiteDescription = async () => {
  try {
    await adminService.updateSetting('site_description', siteDescription.value)
    success('توضیح سایت با موفقیت ذخیره شد')
  } catch (err) {
    error('خطا در ذخیره توضیح')
  }
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
.admin-settings {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.settings-card {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  padding: 1.5rem;
  border-radius: 14px;
  border: 1px solid rgba(226, 232, 240, 0.9);
  background: rgba(255, 255, 255, 0.92);
}

.settings-card:hover {
  box-shadow: var(--admin-glow);
  transform: translateY(-2px);
  transition: all 0.2s ease;
}

.card-header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  border-bottom: 1px solid rgba(226, 232, 240, 0.9);
  padding-bottom: 1rem;
}

.card-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: #1f2937;
}

.card-header p {
  margin: 0;
  font-size: 0.9rem;
  color: #6b7280;
}

.setting-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.logo-preview,
.favicon-preview {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  border: 2px solid rgba(102, 126, 234, 0.15);
  background: rgba(102, 126, 234, 0.05);
  padding: 1rem;
  min-height: 150px;
}

.logo-image,
.favicon-image {
  max-width: 100%;
  max-height: 120px;
  object-fit: contain;
}

.favicon-image {
  max-height: 80px;
  max-width: 80px;
}

.no-logo,
.no-favicon,
.no-images {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  font-size: 0.95rem;
  min-height: 150px;
}

.no-images {
  min-height: 150px;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 10px;
}

.upload-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.file-input-wrapper {
  position: relative;
}

.file-input {
  display: none;
}

.upload-label {
  display: block;
  padding: 0.75rem 1.25rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px;
  cursor: pointer;
  text-align: center;
  font-weight: 600;
  transition: all 0.2s ease;
}

.upload-label:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.url-input {
  display: flex;
  gap: 0.5rem;
}

.url-input-field {
  flex: 1;
  padding: 0.75rem;
  border: 1.5px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
  font-size: 0.95rem;
  font-family: inherit;
}

.url-input-field:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.btn-small {
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
}

.btn-small:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.form-input,
.form-textarea {
  padding: 0.75rem;
  border: 1.5px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
  font-size: 0.95rem;
  font-family: inherit;
  background: white;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.uploading-status {
  padding: 0.5rem;
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 6px;
  text-align: center;
  font-size: 0.85rem;
  font-weight: 600;
}

.card-actions {
  display: flex;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(226, 232, 240, 0.9);
}

.btn-primary {
  padding: 0.7rem 1.25rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
  flex: 1;
  text-align: center;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 22px rgba(102, 126, 234, 0.3);
}

.btn-remove-image {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #ef4444;
  color: white;
  border: 2px solid white;
  font-size: 1.2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.btn-remove-image:hover {
  background: #dc2626;
  transform: scale(1.05);
}

.text-muted {
  color: #6b7280;
  font-size: 0.95rem;
}

/* اسلایدرهای صفحه اصلی */
.sliders-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 1.5rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid rgba(226, 232, 240, 0.9);
  border-radius: 14px;
}

.section-header-local {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  border-bottom: 1px solid rgba(226, 232, 240, 0.9);
  padding-bottom: 1rem;
}

.section-header-local h2 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 700;
  color: #1f2937;
}

.section-header-local p {
  margin: 0;
  font-size: 0.95rem;
  color: #6b7280;
}

.info-box {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.25rem;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 74, 162, 0.08));
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 10px;
}

.info-box p {
  margin: 0;
  color: #4b5563;
  font-size: 0.95rem;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }

  .sliders-grid {
    grid-template-columns: 1fr;
  }

  .url-input {
    flex-direction: column;
  }

  .card-actions {
    flex-direction: column;
  }
}
</style>
