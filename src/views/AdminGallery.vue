<template>
  <div class="admin-gallery admin-page">
    <div class="admin-section-header">
      <div>
        <div class="eyebrow">🎨 مدیریت گالری</div>
        <h2>گالری پروژه‌ها</h2>
        <p class="muted">افزودن و بروزرسانی آیتم‌های گالری و اسلایدر مرتبط</p>
        <div class="meta-chips">
          <span class="chip">{{ items.length }} آیتم</span>
          <span class="chip subtle" v-if="sliders.length">{{ sliders.length }} اسلایدر</span>
        </div>
      </div>
      <div class="header-actions">
        <button @click="showForm = true" class="btn-primary ghost">➕ آیتم جدید</button>
      </div>
    </div>

    <!-- فرم افزودن/ویرایش -->
    <div v-if="showForm" class="modal-overlay" @click.self="closeForm">
      <div class="modal-card admin-modal">
        <div class="modal-header">
          <h2>{{ editingId ? 'ویرایش آیتم' : 'آیتم جدید' }}</h2>
          <button @click="closeForm" class="close-btn">✕</button>
        </div>
        <form @submit.prevent="submitForm" class="gallery-form">
          <div class="form-row">
            <div class="form-group">
              <label>عنوان</label>
              <input v-model="formData.title" type="text" required />
            </div>
            <div class="form-group">
              <label>دسته‌بندی</label>
              <input v-model="formData.category" type="text" required />
            </div>
          </div>

          <div class="form-group">
            <label>توضیح</label>
            <textarea v-model="formData.description" rows="3" required></textarea>
          </div>

          <div class="form-group">
            <label>تصویر شاخص</label>
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

          <div class="form-row">
            <div class="form-group">
              <label>اسلایدر (چندین عکس)</label>
              <select v-model="formData.slider_id">
                <option :value="null">-- انتخاب نکنید --</option>
                <option v-for="slider in sliders" :key="slider.id" :value="slider.id">
                  {{ slider.name }} ({{ slider.images?.length || 0 }} عکس)
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>مدت زمان</label>
              <input v-model="formData.duration" type="text" placeholder="مثال: 2 ساعت" />
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary">{{ editingId ? 'ذخیره تغییرات' : 'ایجاد آیتم' }}</button>
            <button type="button" @click="closeForm" class="btn-secondary">انصراف</button>
          </div>
        </form>
      </div>
    </div>

    <!-- لیست گالری -->
    <div class="panel">
      <div v-if="loading" class="loading">در حال بارگذاری...</div>
      <div v-else-if="items.length === 0" class="empty">
        <p>هیچ آیتمی یافت نشد</p>
      </div>
      <div v-else class="card-grid">
        <div v-for="item in items" :key="item.id" class="card media-card glass-card">
          <div class="media-image">
            <img v-if="item.image" :src="item.image" :alt="item.title" />
            <div v-else class="media-placeholder">{{ item.icon || '🎨' }}</div>
          </div>
          <div class="card-body">
            <div class="card-title">{{ item.title }}</div>
            <div class="card-sub">
              <span class="pill">{{ item.category }}</span>
              <span v-if="item.duration" class="pill subtle">⏱ {{ item.duration }}</span>
            </div>
            <p class="card-text">{{ item.description }}</p>
            <div class="card-actions">
              <button @click="editItem(item)" class="btn-edit">✏️ ویرایش</button>
              <button @click="deleteItem(item.id)" class="btn-delete">🗑️ حذف</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminService } from '../api/services'

const items = ref([])
const sliders = ref([])
const loading = ref(false)
const showForm = ref(false)
const editingId = ref(null)
const uploadingImage = ref(false)
const formData = ref({
  title: '',
  description: '',
  category: '',
  image: '',
  slider_id: null,
  duration: ''
})

const loadItems = async () => {
  loading.value = true
  try {
    items.value = await adminService.getGalleryItems()
    sliders.value = await adminService.getSliders()
  } catch (error) {
    console.error('Failed to load gallery items:', error)
    try { const { error: tError } = await import('../composables/useToast.js'); tError('خطا در بارگذاری آیتم‌های گالری'); } catch {}
  } finally {
    loading.value = false
  }
}

const editItem = (item) => {
  editingId.value = item.id
  formData.value = { ...item }
  showForm.value = true
}

const submitForm = async () => {
  try {
    if (editingId.value) {
      await adminService.updateGalleryItem(editingId.value, formData.value)
      try { const { success } = await import('../composables/useToast.js'); success('آیتم بروزرسانی شد'); } catch {}
    } else {
      await adminService.createGalleryItem(formData.value)
      try { const { success } = await import('../composables/useToast.js'); success('آیتم ایجاد شد'); } catch {}
    }
    closeForm()
    await loadItems()
  } catch (error) {
    try { const { error: tError } = await import('../composables/useToast.js'); tError(error.response?.data?.detail || 'خطا در ذخیره آیتم'); } catch {}
  }
}

const deleteItem = async (id) => {
  if (!confirm('آیا از حذف این آیتم مطمئن هستید؟')) return
  
  try {
    await adminService.deleteGalleryItem(id)
    try { const { success } = await import('../composables/useToast.js'); success('آیتم حذف شد'); } catch {}
    await loadItems()
  } catch (error) {
    try { const { error: tError } = await import('../composables/useToast.js'); tError(error.response?.data?.detail || 'خطا در حذف آیتم'); } catch {}
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
    try { const { error: tError } = await import('../composables/useToast.js'); tError(error.response?.data?.detail || 'خطا در آپلود تصویر'); } catch {}
  } finally {
    uploadingImage.value = false
  }
}

const closeForm = () => {
  showForm.value = false
  editingId.value = null
  formData.value = {
    title: '',
    description: '',
    category: '',
    image: '',
    slider_id: null,
    duration: ''
  }
}

onMounted(() => {
  loadItems()
})
</script>

<style scoped>
.admin-gallery { display: flex; flex-direction: column; gap: 1.5rem; }
.header-actions { display: flex; gap: 0.75rem; }

.gallery-form { display: flex; flex-direction: column; gap: 1rem; padding: 1.25rem 1.5rem; }
.file-input-group { display: flex; flex-direction: column; gap: 0.65rem; }
.uploading-status { font-weight: 700; color: #4338ca; }

.card-text { color: #4b5563; line-height: 1.6; }

.form-actions { justify-content: flex-end; flex-wrap: wrap; }

@media (max-width: 768px) {
  .header-actions { width: 100%; justify-content: flex-start; }
}
</style>
