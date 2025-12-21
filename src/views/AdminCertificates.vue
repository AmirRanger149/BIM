<template>
  <div class="admin-certificates admin-page">
    <div class="section-header">
      <h2>📜 مدیریت گواهینامه‌ها و استانداردها</h2>
      <button @click="openAddDialog" class="btn-add">
        ➕ افزودن گواهینامه
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>بارگذاری اطلاعات...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="certificates.length === 0" class="empty-state">
      <div class="empty-icon">📋</div>
      <p>هنوز گواهینامه‌ای ثبت نشده است.</p>
      <button @click="openAddDialog" class="btn-add-empty">افزودن گواهینامه اول</button>
    </div>

    <!-- Certificates Grid -->
    <div v-else class="certificates-grid">
      <div v-for="cert in certificates" :key="cert.id" class="certificate-card">
        <div class="cert-header">
          <div class="cert-icon" :style="{ backgroundColor: cert.color || '#0ea5e9' }">
            {{ cert.icon }}
          </div>
          <div class="cert-actions">
            <button @click="editCertificate(cert)" class="btn-icon" title="ویرایش">
              ✏️
            </button>
            <button @click="deleteCertificate(cert.id)" class="btn-icon danger" title="حذف">
              🗑️
            </button>
          </div>
        </div>
        
        <div class="cert-content">
          <h3 class="cert-title">{{ cert.title }}</h3>
          <p class="cert-issuer">{{ cert.issuer }}</p>
          
          <div class="cert-meta">
            <span v-if="cert.date" class="cert-date">📅 {{ cert.date }}</span>
            <span v-if="cert.type_label" class="cert-badge" :class="cert.type">
              {{ cert.type_label }}
            </span>
          </div>
          
          <p v-if="cert.description" class="cert-description">
            {{ cert.description }}
          </p>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showDialog" class="modal-overlay" @click="closeDialog">
          <div class="modal-content" @click.stop>
            <div class="modal-header">
              <h3>{{ editingId ? 'ویرایش گواهینامه' : 'افزودن گواهینامه جدید' }}</h3>
              <button @click="closeDialog" class="btn-close">✕</button>
            </div>

            <form @submit.prevent="saveCertificate" class="certificate-form">
              <div class="form-group">
                <label for="cert-title">نام گواهینامه *</label>
                <input
                  id="cert-title"
                  v-model="formData.title"
                  type="text"
                  placeholder="مثلاً: گواهینامه تخصصی Vue.js"
                  required
                />
              </div>

              <div class="form-group">
                <label for="cert-issuer">سازمان صادر‌کننده *</label>
                <input
                  id="cert-issuer"
                  v-model="formData.issuer"
                  type="text"
                  placeholder="مثلاً: Vue School"
                  required
                />
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="cert-date">تاریخ</label>
                  <input
                    id="cert-date"
                    v-model="formData.date"
                    type="text"
                    placeholder="مثلاً: ۲۰۲۴"
                  />
                </div>

                <div class="form-group">
                  <label for="cert-icon">آیکون</label>
                  <input
                    id="cert-icon"
                    v-model="formData.icon"
                    type="text"
                    placeholder="مثلاً: ⚡"
                    maxlength="2"
                  />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="cert-color">رنگ</label>
                  <input
                    id="cert-color"
                    v-model="formData.color"
                    type="color"
                    title="انتخاب رنگ"
                  />
                </div>

                <div class="form-group">
                  <label for="cert-type">نوع</label>
                  <select id="cert-type" v-model="formData.type">
                    <option value="">بدون نوع</option>
                    <option value="certificate">گواهینامه</option>
                    <option value="standard">استاندارد</option>
                    <option value="qualification">مدرک</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label for="cert-gradient">Gradient</label>
                <input
                  id="cert-gradient"
                  v-model="formData.gradient"
                  type="text"
                  placeholder="مثلاً: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)"
                />
              </div>

              <div class="form-group">
                <label for="cert-image">تصویر شاخص</label>
                <div class="image-upload-group">
                  <input
                    type="file"
                    accept="image/*"
                    @change="handleImageUpload"
                    :disabled="uploading"
                    class="file-input"
                  />
                  <div v-if="uploading" class="upload-status">در حال آپلود...</div>
                  <div v-if="formData.image" class="image-preview">
                    <img :src="formData.image" alt="پیش‌نمایش" />
                    <button type="button" @click="formData.image = ''" class="btn-remove-image">×</button>
                  </div>
                </div>
              </div>

              <div class="form-group">
                <label for="cert-slider">اسلایدر</label>
                <select id="cert-slider" v-model.number="formData.slider_id">
                  <option :value="null">بدون اسلایدر</option>
                  <option v-for="slider in sliders" :key="slider.id" :value="slider.id">
                    {{ slider.name }} ({{ slider.images?.length || 0 }} تصویر)
                  </option>
                </select>
                <small class="form-hint">برای نمایش چندین تصویر به صورت اسلایدر</small>
              </div>

              <div class="form-group">
                <label for="cert-type-label">برچسب نوع (متن)</label>
                <input
                  id="cert-type-label"
                  v-model="formData.type_label"
                  type="text"
                  placeholder="مثلاً: معتبر"
                />
              </div>

              <div class="form-group">
                <label for="cert-description">توضیح</label>
                <textarea
                  id="cert-description"
                  v-model="formData.description"
                  placeholder="توضیح کوتاهی درباره این گواهینامه..."
                  rows="4"
                ></textarea>
              </div>

              <div class="form-actions">
                <button type="button" @click="closeDialog" class="btn-cancel">
                  انصراف
                </button>
                <button type="submit" class="btn-submit">
                  {{ editingId ? 'بروزرسانی' : 'افزودن' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Confirmation Dialog -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showConfirm" class="modal-overlay" @click="showConfirm = false">
          <div class="confirm-dialog" @click.stop>
            <p>آیا از حذف این گواهینامه اطمینان دارید؟</p>
            <div class="confirm-actions">
              <button @click="showConfirm = false" class="btn-cancel">انصراف</button>
              <button @click="confirmDelete" class="btn-delete">حذف</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminService } from '../api/services'

const certificates = ref([])
const sliders = ref([])
const loading = ref(true)
const uploading = ref(false)
const showDialog = ref(false)
const showConfirm = ref(false)
const editingId = ref(null)
const deleteTargetId = ref(null)

const formData = ref({
  title: '',
  issuer: '',
  date: '',
  description: '',
  icon: '📜',
  color: '#0ea5e9',
  gradient: '',
  image: '',
  slider_id: null,
  type: '',
  type_label: ''
})

const resetForm = () => {
  formData.value = {
    title: '',
    issuer: '',
    date: '',
    description: '',
    icon: '📜',
    color: '#0ea5e9',
    gradient: '',
    image: '',
    slider_id: null,
    type: '',
    type_label: ''
  }
}

const openAddDialog = () => {
  editingId.value = null
  resetForm()
  showDialog.value = true
}

const editCertificate = (cert) => {
  editingId.value = cert.id
  formData.value = {
    title: cert.title,
    issuer: cert.issuer,
    date: cert.date || '',
    description: cert.description || '',
    icon: cert.icon || '📜',
    color: cert.color || '#0ea5e9',
    gradient: cert.gradient || '',
    image: cert.image || '',
    slider_id: cert.slider_id || null,
    type: cert.type || '',
    type_label: cert.type_label || ''
  }
  showDialog.value = true
}

const closeDialog = () => {
  showDialog.value = false
  editingId.value = null
  resetForm()
}

const saveCertificate = async () => {
  try {
    if (editingId.value) {
      await adminService.updateCertificate(editingId.value, formData.value)
      try { const { success } = await import('../composables/useToast.js'); success('گواهینامه بروزرسانی شد'); } catch {}
    } else {
      await adminService.createCertificate(formData.value)
      try { const { success } = await import('../composables/useToast.js'); success('گواهینامه با موفقیت اضافه شد'); } catch {}
    }
    
    await fetchCertificates()
    closeDialog()
  } catch (error) {
    console.error('خطا در ذخیره گواهینامه:', error)
    try { const { error: tError } = await import('../composables/useToast.js'); tError('خطا در ذخیره گواهینامه'); } catch {}
  }
}

const deleteCertificate = (id) => {
  deleteTargetId.value = id
  showConfirm.value = true
}

const confirmDelete = async () => {
  try {
    await adminService.deleteCertificate(deleteTargetId.value)
    try { const { success } = await import('../composables/useToast.js'); success('گواهینامه حذف شد'); } catch {}
    await fetchCertificates()
    showConfirm.value = false
    deleteTargetId.value = null
  } catch (error) {
    console.error('خطا در حذف گواهینامه:', error)
    try { const { error: tError } = await import('../composables/useToast.js'); tError('خطا در حذف گواهینامه'); } catch {}
  }
}

const fetchCertificates = async () => {
  try {
    loading.value = true
    const response = await adminService.getCertificates()
    certificates.value = Array.isArray(response) ? response : response.data || []
  } catch (error) {
    console.error('خطا در دریافت گواهینامه‌ها:', error)
    certificates.value = []
    try { const { error: tError } = await import('../composables/useToast.js'); tError('خطا در دریافت گواهینامه‌ها'); } catch {}
  } finally {
    loading.value = false
  }
}

const fetchSliders = async () => {
  try {
    const response = await adminService.getSliders()
    sliders.value = Array.isArray(response) ? response : response.data || []
  } catch (error) {
    console.error('خطا در دریافت اسلایدرها:', error)
    sliders.value = []
  }
}

const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  try {
    uploading.value = true
    const uploadedUrl = await adminService.uploadImage(file)
    formData.value.image = uploadedUrl
  } catch (error) {
    console.error('خطا در آپلود تصویر:', error)
    try { const { error: tError } = await import('../composables/useToast.js'); tError('خطا در آپلود تصویر'); } catch {}
  } finally {
    uploading.value = false
  }
}

onMounted(() => {
  fetchCertificates()
  fetchSliders()
})
</script>

<style scoped>
/* This view now uses the global admin theme (admin.css). */
.empty-icon { font-size: 3rem; }
</style>
