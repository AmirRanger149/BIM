<template>
  <div class="admin-sliders admin-page">
    <div class="admin-section-header">
      <div>
        <div class="eyebrow">🎬 مدیریت اسلایدر</div>
        <h2>اسلایدهای اصلی و هدر</h2>
        <p class="muted">افزودن، ویرایش و چیدمان تصاویر قهرمان صفحه</p>
        <div class="meta-chips">
          <span class="chip">{{ sliders.length }} اسلایدر</span>
          <span class="chip subtle">{{ totalImages }} تصویر کل</span>
        </div>
      </div>
      <div class="header-actions">
        <button @click="showForm = true" class="btn-primary ghost">➕ اسلایدر جدید</button>
      </div>
    </div>

    <!-- فرم افزودن/ویرایش -->
    <div v-if="showForm" class="modal-overlay" @click.self="closeForm">
      <div class="modal-card admin-modal">
        <div class="modal-header">
          <h2>{{ editingId ? 'ویرایش اسلایدر' : 'اسلایدر جدید' }}</h2>
          <button @click="closeForm" class="close-btn">✕</button>
        </div>
        <form @submit.prevent="submitForm" class="slider-form">
          <div class="form-group">
            <label>نام اسلایدر</label>
            <input v-model="formData.name" type="text" required />
          </div>

          <div class="form-group">
            <label>توضیح (اختیاری)</label>
            <textarea v-model="formData.description" rows="2"></textarea>
          </div>

          <div class="form-group">
            <label>تصاویر در اسلایدر</label>
            <div class="images-manager">
              <div class="add-images">
                <div class="file-input-wrapper">
                  <input
                    type="file"
                    @change="handleImageUpload"
                    accept="image/*"
                    class="file-input"
                    multiple
                  />
                  <span class="upload-label">📁 انتخاب تصاویر</span>
                </div>
                <div class="url-input">
                  <input v-model="newImageUrl" type="url" placeholder="یا URL تصویر را پیوند کنید" />
                  <button type="button" @click="addImageUrl" class="btn-small">اضافه کنید</button>
                </div>
                <div v-if="uploadingImage" class="uploading-status">درحال آپلود...</div>
              </div>

              <div class="images-preview">
                <h4>تصاویر انتخاب‌شده ({{ formData.images.length }})</h4>
                <div v-if="formData.images.length === 0" class="no-images">
                  هنوز تصویری اضافه نشده است
                </div>
                <div v-else class="images-list">
                  <div v-for="(image, index) in formData.images" :key="index" class="image-item">
                    <img :src="image" :alt="`Image ${index + 1}`" />
                    <button type="button" @click="removeImage(index)" class="btn-remove">✕</button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary">{{ editingId ? 'ذخیره تغییرات' : 'ایجاد اسلایدر' }}</button>
            <button type="button" @click="closeForm" class="btn-secondary">انصراف</button>
          </div>
        </form>
      </div>
    </div>

    <!-- لیست اسلایدرها -->
    <div class="panel">
      <div v-if="loading" class="loading">در حال بارگذاری...</div>
      <div v-else-if="sliders.length === 0" class="empty">
        <p>هیچ اسلایدری یافت نشد</p>
      </div>
      <div v-else class="sliders-grid">
        <div v-for="slider in sliders" :key="slider.id" class="slider-card glass-card">
          <div class="card-preview">
            <div v-if="slider.images && slider.images.length > 0" class="preview-images">
              <img
                v-for="(image, idx) in slider.images.slice(0, 3)"
                :key="idx"
                :src="image"
                :alt="`Image ${idx + 1}`"
                class="preview-img"
              />
              <div v-if="slider.images.length > 3" class="more-count">
                +{{ slider.images.length - 3 }}
              </div>
            </div>
            <div v-else class="no-preview">🖼️ بدون تصویر</div>
          </div>
          <div class="card-content">
            <h3>{{ slider.name }}</h3>
            <p v-if="slider.description" class="description">{{ slider.description }}</p>
            <div class="images-count">📷 {{ slider.images ? slider.images.length : 0 }} تصویر</div>
          </div>
          <div class="card-actions">
            <button @click.stop="editSlider(slider)" class="btn-edit">✏️ ویرایش</button>
            <button @click.stop="deleteSlider(slider.id)" class="btn-delete">🗑️ حذف</button>
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

const sliders = ref([])
const loading = ref(false)
const showForm = ref(false)
const editingId = ref(null)
const uploadingImage = ref(false)
const newImageUrl = ref('')
const formData = ref({
  name: '',
  description: '',
  images: []
})

const totalImages = computed(() => sliders.value.reduce((sum, s) => sum + (s.images?.length || 0), 0))

const loadSliders = async () => {
  loading.value = true
  try {
    sliders.value = await adminService.getSliders()
  } catch (err) {
    console.error('Failed to load sliders:', err)
    notifyError('خطا در بارگذاری اسلایدرها')
  } finally {
    loading.value = false
  }
}

const editSlider = (slider) => {
  editingId.value = slider.id
  formData.value = { ...slider }
  showForm.value = true
}

const submitForm = async () => {
  try {
    if (editingId.value) {
      await adminService.updateSlider(editingId.value, formData.value)
      notifySuccess('اسلایدر به‌روزرسانی شد')
    } else {
      await adminService.createSlider(formData.value)
      notifySuccess('اسلایدر ایجاد شد')
    }
    closeForm()
    await loadSliders()
  } catch (err) {
    notifyError(err.response?.data?.detail || 'عملیات ناموفق')
  }
}

const deleteSlider = async (id) => {
  if (!confirm('آیا از حذف این اسلایدر مطمئن هستید؟')) return
  try {
    await adminService.deleteSlider(id)
    notifySuccess('اسلایدر حذف شد')
    await loadSliders()
  } catch (err) {
    notifyError(err.response?.data?.detail || 'عملیات ناموفق')
  }
}

const addImageUrl = () => {
  if (!newImageUrl.value.trim()) return
  if (!formData.value.images) formData.value.images = []
  formData.value.images.push(newImageUrl.value.trim())
  newImageUrl.value = ''
}

const removeImage = (index) => {
  formData.value.images.splice(index, 1)
}

const closeForm = () => {
  showForm.value = false
  editingId.value = null
  newImageUrl.value = ''
  formData.value = { name: '', description: '', images: [] }
}

const handleImageUpload = async (event) => {
  const files = event.target.files
  if (!files || files.length === 0) return

  uploadingImage.value = true
  try {
    if (!formData.value.images) formData.value.images = []
    for (const file of files) {
      const formDataFile = new FormData()
      formDataFile.append('file', file)
      const response = await adminService.uploadFile(formDataFile)
      formData.value.images.push(response.url)
    }
    notifySuccess('تصاویر آپلود شد')
  } catch (err) {
    notifyError(err.response?.data?.detail || 'خطا در آپلود تصویر')
  } finally {
    uploadingImage.value = false
  }
}

onMounted(() => {
  loadSliders()
})

const notifySuccess = (message) => {
  try { success(message) } catch (err) { console.error(message, err) }
}

const notifyError = (message) => {
  try { error(message) } catch (err) { console.error(message, err) }
}
</script>

<style scoped>
.admin-sliders { display: flex; flex-direction: column; gap: 1.5rem; }
.header-actions { display: flex; gap: 0.75rem; flex-wrap: wrap; }
.slider-form { padding: 1.25rem 1.5rem; display: flex; flex-direction: column; gap: 1rem; }
.images-manager { display: flex; flex-direction: column; gap: 1rem; border: 1px dashed rgba(102,126,234,0.25); border-radius: 12px; padding: 1rem; background: rgba(255,255,255,0.9); }
.images-preview h4 { margin: 0 0 0.75rem 0; color: #1f2937; }
.images-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 0.65rem; }
.image-item { position: relative; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.08); aspect-ratio: 1; }
.image-item img { width: 100%; height: 100%; object-fit: cover; }
.btn-remove { position: absolute; top: 6px; right: 6px; background: rgba(0,0,0,0.6); color: white; border: none; border-radius: 50%; width: 24px; height: 24px; cursor: pointer; }
.preview-images { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.4rem; width: 100%; height: 100%; }
.preview-img { width: 100%; height: 100%; object-fit: cover; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.more-count { display: flex; align-items: center; justify-content: center; background: rgba(102,126,234,0.12); border: 1px dashed #0ea5e9; color: #4338ca; font-weight: 700; border-radius: 10px; padding: 0.3rem 0.75rem; }
.form-actions { display: flex; gap: 0.75rem; justify-content: flex-end; margin-top: 0.25rem; }

.sliders-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.25rem; }
.slider-card { border: 1px solid rgba(226,232,240,0.9); border-radius: 14px; overflow: hidden; display: flex; flex-direction: column; transition: transform 0.2s ease, box-shadow 0.25s ease; background: rgba(255,255,255,0.92); }
.slider-card:hover { transform: translateY(-4px); box-shadow: var(--admin-glow); }
.card-preview { width: 100%; height: 200px; background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%); display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; overflow: hidden; position: relative; }
.no-preview { grid-column: 1 / -1; display: flex; align-items: center; justify-content: center; font-size: 2rem; color: #e5e7eb; }
.card-content { padding: 1.1rem; flex: 1; display: flex; flex-direction: column; gap: 0.65rem; }
.card-content h3 { margin: 0; font-size: 1.05rem; color: #111827; font-weight: 700; }
.description { margin: 0; font-size: 0.9rem; color: #4b5563; line-height: 1.6; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.images-count { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.35rem 0.75rem; background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%); color: white; border-radius: 10px; font-size: 0.85rem; font-weight: 700; width: fit-content; }
.card-actions { display: flex; gap: 0.5rem; padding: 0.9rem 1rem; border-top: 1px solid rgba(226,232,240,0.9); margin-top: auto; }
.btn-edit, .btn-delete { flex: 1; padding: 0.6rem 0.75rem; background: none; border: 1px solid #e2e8f0; border-radius: 8px; cursor: pointer; font-size: 0.9rem; transition: all 0.2s; font-weight: 700; white-space: nowrap; }
.btn-edit:hover { background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%); border-color: #0ea5e9; color: white; }
.btn-delete:hover { background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%); border-color: #06b6d4; color: white; }

@media (max-width: 768px) {
  .header-actions { width: 100%; justify-content: flex-start; }
  .sliders-grid { grid-template-columns: 1fr; }
  .card-preview { height: 180px; }
}
</style>
