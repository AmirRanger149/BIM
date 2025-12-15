<template>
  <div class="admin-testimonials admin-page">
    <div class="admin-section-header">
      <div>
        <div class="eyebrow">💬 بازخوردها</div>
        <h2>نظر مشتریان</h2>
        <p class="muted">مدیریت تایید، ویرایش و اضافه کردن نظرات جدید</p>
        <div class="meta-chips">
          <span class="chip">{{ testimonials.length }} نظر</span>
          <span class="chip subtle">در انتظار تایید {{ pendingCount }}</span>
        </div>
      </div>
      <div class="header-actions">
        <button @click="showForm = true" class="btn-primary">➕ نظر جدید</button>
      </div>
    </div>

    <!-- فرم افزودن/ویرایش -->
    <div v-if="showForm" class="modal-overlay" @click.self="closeForm">
      <div class="modal-card admin-modal">
        <div class="modal-header">
          <h2>{{ editingId ? 'ویرایش نظر' : 'نظر جدید' }}</h2>
          <button @click="closeForm" class="close-btn">✕</button>
        </div>
        <form @submit.prevent="submitForm" class="testimonial-form">
          <div class="form-row">
            <div class="form-group">
              <label>نام</label>
              <input v-model="formData.name" type="text" required />
            </div>
            <div class="form-group">
              <label>عنوان/شغل</label>
              <input v-model="formData.role" type="text" required />
            </div>
          </div>

          <div class="form-group">
            <label>نظر</label>
            <textarea v-model="formData.text" rows="4" required></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>امتیاز (1-5)</label>
              <input v-model.number="formData.rating" type="number" min="1" max="5" />
            </div>
            <div class="form-group">
              <label>پروژه</label>
              <input v-model="formData.project" type="text" />
            </div>
          </div>

          <div class="form-group">
            <label>تصویر پروفایل (URL یا آپلود)</label>
            <div class="file-input-group">
              <input 
                type="file" 
                @change="handleImageUpload" 
                accept="image/*"
                class="file-input"
              />
              <input v-model="formData.image" type="text" placeholder="یا URL تصویر را پیوند کنید" />
            </div>
            <div v-if="uploadingImage" class="uploading-status">درحال آپلود...</div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary">{{ editingId ? 'ذخیره تغییرات' : 'ایجاد نظر' }}</button>
            <button type="button" @click="closeForm" class="btn-secondary">انصراف</button>
          </div>
        </form>
      </div>
    </div>

    <!-- لیست نظرات -->
    <div class="panel">
      <div v-if="loading" class="loading">در حال بارگذاری...</div>
      <div v-else-if="testimonials.length === 0" class="empty">
        <p>هیچ نظری یافت نشد</p>
      </div>
      <div v-else>
        <div class="testimonials-container scroll-area">
          <div 
            v-for="testimonial in testimonials" 
            :key="testimonial.id" 
            class="testimonial-card glass-card" 
            :class="{ pending: !testimonial.approved }"
          >
            <div class="testimonial-header">
              <div class="user-info">
                <div class="avatar">{{ testimonial.avatar || '👤' }}</div>
                <div class="info">
                  <h3>{{ testimonial.name }}</h3>
                  <p>{{ testimonial.role }}</p>
                </div>
              </div>
              <div class="rating">
                <span v-for="i in testimonial.rating" :key="i">⭐</span>
              </div>
            </div>

            <div class="testimonial-text">
              {{ testimonial.text }}
            </div>

            <div v-if="testimonial.project" class="project-tag">
              {{ testimonial.project }}
            </div>

            <div class="testimonial-actions">
              <button 
                v-if="!testimonial.approved"
                @click="approveTestimonial(testimonial.id)"
                class="btn-small"
              >
                ✓ تایید
              </button>
              <span v-else class="approved-badge">✓ تایید شده</span>
              <button @click="editTestimonial(testimonial)" class="btn-edit">✏️</button>
              <button @click="deleteTestimonial(testimonial.id)" class="btn-delete">🗑️</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { adminService } from '../api/services'
import { success, error } from '../composables/useToast.js'

const testimonials = ref([])
const loading = ref(false)
const showForm = ref(false)
const editingId = ref(null)
const uploadingImage = ref(false)
const formData = ref({
  name: '',
  role: '',
  text: '',
  rating: 5,
  project: '',
  image: '',
  avatar: '👤'
})

const pendingCount = computed(() => testimonials.value.filter(t => !t.approved).length)

const loadTestimonials = async () => {
  loading.value = true
  try {
    testimonials.value = await adminService.getTestimonials()
  } catch (error) {
    console.error('Failed to load testimonials:', error)
    notifyError('خطا در بارگذاری نظرات')
  } finally {
    loading.value = false
  }
}

const editTestimonial = (testimonial) => {
  editingId.value = testimonial.id
  formData.value = { ...testimonial }
  showForm.value = true
}

const submitForm = async () => {
  try {
    if (editingId.value) {
      await adminService.updateTestimonial(editingId.value, formData.value)
      notifySuccess('نظر به‌روزرسانی شد')
    } else {
      await adminService.createTestimonial(formData.value)
      notifySuccess('نظر ایجاد شد')
    }
    closeForm()
    await loadTestimonials()
  } catch (error) {
    notifyError(error.response?.data?.detail || 'عملیات ناموفق')
  }
}

const approveTestimonial = async (id) => {
  try {
    await adminService.approveTestimonial(id)
    notifySuccess('نظر تایید شد')
    await loadTestimonials()
  } catch (error) {
    notifyError(error.response?.data?.detail || 'عملیات ناموفق')
  }
}

const deleteTestimonial = async (id) => {
  if (!confirm('آیا از حذف این نظر مطمئن هستید؟')) return
  
  try {
    await adminService.deleteTestimonial(id)
    notifySuccess('نظر حذف شد')
    await loadTestimonials()
  } catch (error) {
    notifyError(error.response?.data?.detail || 'عملیات ناموفق')
  }
}

const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  uploadingImage.value = true
  try {
    const formDataFile = new FormData()
    formDataFile.append('file', file)
    const response = await adminService.uploadFile(formDataFile)
    formData.value.image = response.url
  } catch (error) {
    notifyError(error.response?.data?.detail || 'خطا در آپلود تصویر')
  } finally {
    uploadingImage.value = false
  }
}

const closeForm = () => {
  showForm.value = false
  editingId.value = null
  formData.value = {
    name: '',
    role: '',
    text: '',
    rating: 5,
    project: '',
    image: '',
    avatar: '👤'
  }
}

onMounted(() => {
  loadTestimonials()
})

const notifySuccess = (message) => {
  try { success(message) } catch (err) { console.error(message, err) }
}

const notifyError = (message) => {
  try { error(message) } catch (err) { console.error(message, err) }
}
</script>

<style scoped>
.admin-testimonials { display: flex; flex-direction: column; gap: 1.5rem; }
.header-actions { display: flex; align-items: center; gap: 0.75rem; }
.testimonials-container { display: grid; gap: 1rem; }
.testimonial-card { padding: 1.25rem; border-radius: 14px; border: 1px solid rgba(226,232,240,0.9); transition: transform 0.2s ease, box-shadow 0.25s ease; }
.testimonial-card.pending { border-left: 4px solid #fb923c; background: linear-gradient(135deg, rgba(255,247,237,0.9), rgba(255,255,255,0.96)); }
.testimonial-header { display: flex; justify-content: space-between; gap: 1rem; align-items: flex-start; margin-bottom: 0.75rem; }
.user-info { display: flex; gap: 0.9rem; align-items: center; }
.avatar { width: 52px; height: 52px; font-size: 1.6rem; background: linear-gradient(135deg, #eef2ff, #f5f3ff); color: #4338ca; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; }
.info h3 { margin: 0; font-size: 1.05rem; color: #0f172a; }
.info p { margin: 0.15rem 0 0; color: #6b7280; font-weight: 600; }
.rating { display: flex; gap: 0.15rem; font-size: 1.05rem; }
.testimonial-text { color: #374151; line-height: 1.7; margin: 0 0 0.75rem; }
.project-tag { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.3rem 0.75rem; border-radius: 999px; background: rgba(102,126,234,0.12); color: #4338ca; font-weight: 700; font-size: 0.9rem; margin-bottom: 0.75rem; }
.testimonial-actions { display: flex; gap: 0.45rem; align-items: center; flex-wrap: wrap; }
.approved-badge { background: #d1fae5; color: #065f46; padding: 0.45rem 0.85rem; border-radius: 10px; font-weight: 800; font-size: 0.85rem; }
@media (max-width: 768px) {
  .testimonial-header { flex-direction: column; align-items: flex-start; }
}
</style>
