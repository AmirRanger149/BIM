<template>
  <div class="admin-articles admin-page">
    <div class="admin-section-header">
      <div>
        <div class="eyebrow">📝 مدیریت مقالات</div>
        <h2>مقالات</h2>
        <p class="muted">ایجاد، ویرایش و مدیریت انتشار مقالات سایت</p>
        <div class="meta-chips">
          <span class="chip">{{ articles.length }} مقاله</span>
          <span class="chip subtle" v-if="sliders.length">{{ sliders.length }} اسلایدر موجود</span>
        </div>
      </div>
      <div class="header-actions">
        <button @click="showForm = true" class="btn-primary ghost">
          ➕ مقاله جدید
        </button>
      </div>
    </div>

    <!-- فرم افزودن/ویرایش -->
    <div v-if="showForm" class="modal-overlay" @click.self="closeForm">
      <div class="modal-card">
        <div class="modal-header">
          <h2>{{ editingId ? 'ویرایش مقاله' : 'مقاله جدید' }}</h2>
          <button @click="closeForm" class="close-btn">✕</button>
        </div>
        <form @submit.prevent="submitForm" class="article-form">
          <div class="form-row">
            <div class="form-group">
              <label>عنوان</label>
              <input v-model="formData.title" type="text" required />
            </div>
            <div class="form-group">
              <label>نویسنده</label>
              <input v-model="formData.author" type="text" required />
            </div>
          </div>

          <div class="form-group">
            <label>خلاصه</label>
            <textarea v-model="formData.excerpt" rows="3" required></textarea>
          </div>

          <div class="form-group">
            <label>محتوای کامل</label>
            <textarea v-model="formData.full_content" rows="6" required></textarea>
          </div>

          <div class="form-group">
            <label>دسته‌بندی</label>
            <input v-model="formData.category" type="text" required />
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

          <div class="form-group">
            <label>اسلایدر (چندین عکس)</label>
            <select v-model="formData.slider_id">
              <option :value="null">-- انتخاب نکنید --</option>
              <option v-for="slider in sliders" :key="slider.id" :value="slider.id">
                {{ slider.name }} ({{ slider.images?.length || 0 }} عکس)
              </option>
            </select>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary">{{ editingId ? 'ذخیره تغییرات' : 'ایجاد مقاله' }}</button>
            <button type="button" @click="closeForm" class="btn-secondary">انصراف</button>
          </div>
        </form>
      </div>
    </div>

    <!-- لیست مقالات -->
    <div class="articles-list">
      <div v-if="loading" class="loading">در حال بارگذاری...</div>
      <div v-else-if="articles.length === 0" class="empty">
        <p>هیچ مقاله‌ای یافت نشد</p>
      </div>
      <div v-else>
        <div class="table-wrapper">
          <table class="articles-table frosted-table">
            <thead>
              <tr>
                <th>عنوان</th>
                <th>نویسنده</th>
                <th>دسته‌بندی</th>
                <th>تاریخ ایجاد</th>
                <th>عملیات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="article in articles" :key="article.id">
                <td>{{ article.title }}</td>
                <td>{{ article.author }}</td>
                <td><span class="pill">{{ article.category }}</span></td>
                <td>{{ formatDate(article.created_at) }}</td>
                <td class="actions">
                  <button @click="editArticle(article)" class="btn-edit">✏️</button>
                  <button @click="deleteArticle(article.id)" class="btn-delete">🗑️</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminService } from '../api/services'

const articles = ref([])
const sliders = ref([])
const loading = ref(false)
const showForm = ref(false)
const editingId = ref(null)
const uploadingImage = ref(false)
const formData = ref({
  title: '',
  excerpt: '',
  full_content: '',
  category: '',
  author: '',
  image: '',
  slider_id: null
})

const loadArticles = async () => {
  loading.value = true
  try {
    articles.value = await adminService.getArticles()
    sliders.value = await adminService.getSliders()
  } catch (error) {
    console.error('Failed to load articles:', error)
    try { const { error: tError } = await import('../composables/useToast.js'); tError('خطا در بارگذاری مقالات'); } catch {}
  } finally {
    loading.value = false
  }
}

const editArticle = (article) => {
  editingId.value = article.id
  formData.value = { ...article }
  showForm.value = true
}

const submitForm = async () => {
  try {
    if (editingId.value) {
      await adminService.updateArticle(editingId.value, formData.value)
      try { const { success } = await import('../composables/useToast.js'); success('مقاله بروزرسانی شد'); } catch {}
    } else {
      await adminService.createArticle(formData.value)
      try { const { success } = await import('../composables/useToast.js'); success('مقاله ایجاد شد'); } catch {}
    }
    closeForm()
    await loadArticles()
  } catch (error) {
    try { const { error: tError } = await import('../composables/useToast.js'); tError(error.response?.data?.detail || 'خطا در ذخیره مقاله'); } catch {}
  }
}

const deleteArticle = async (id) => {
  if (!confirm('آیا از حذف این مقاله مطمئن هستید؟')) return 
  
  try {
    await adminService.deleteArticle(id)
    try { const { success } = await import('../composables/useToast.js'); success('مقاله حذف شد'); } catch {}
    await loadArticles()
  } catch (error) {
    try { const { error: tError } = await import('../composables/useToast.js'); tError(error.response?.data?.detail || 'خطا در حذف مقاله'); } catch {}
  }
}

const closeForm = () => {
  showForm.value = false
  editingId.value = null
  formData.value = {
    title: '',
    excerpt: '',
    full_content: '',
    category: '',
    author: '',
    image: '',
    slider_id: null
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('fa-IR')
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

onMounted(() => {
  loadArticles()
})
</script>

<style scoped>
/* This view now uses the global admin theme (admin.css) with a few local touches. */
.header-actions { display: flex; gap: 1rem; flex-wrap: wrap; }
.meta-chips { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.75rem; }
.chip { padding: 0.35rem 0.85rem; border-radius: 999px; background: rgba(102,126,234,0.12); color: #4338ca; font-weight: 700; font-size: 0.85rem; }
.chip.subtle { background: rgba(67,56,202,0.08); color: #312e81; }
.pill { display: inline-flex; padding: 0.25rem 0.65rem; border-radius: 999px; background: rgba(99,102,241,0.1); color: #3730a3; font-weight: 700; font-size: 0.85rem; }
.frosted-table thead { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; }
.frosted-table tbody tr:hover { background: rgba(102,126,234,0.08); }
.ghost { box-shadow: inset 0 0 0 1px rgba(255,255,255,0.4); }
</style>
