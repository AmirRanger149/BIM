<template>
  <div class="admin-users admin-page">
    <div class="admin-section-header">
      <div>
        <div class="eyebrow">👤 مدیریت کاربران</div>
        <h2>کاربران و نقش‌ها</h2>
        <p class="muted">افزودن، ویرایش، فعال/غیرفعال و نقش ادمین</p>
        <div class="meta-chips">
          <span class="chip">{{ users.length }} کاربر</span>
          <span class="chip subtle">{{ adminCount }} ادمین</span>
          <span class="chip subtle">فعال {{ activeCount }}</span>
        </div>
      </div>
      <div class="header-actions">
        <button class="btn-primary ghost" @click="openCreate">➕ کاربر جدید</button>
      </div>
    </div>

    <div class="panel">
      <div v-if="loading" class="loading">در حال بارگذاری...</div>
      <div v-else-if="users.length === 0" class="empty">هنوز کاربری ثبت نشده است</div>
      <div v-else class="table-wrapper">
        <table class="users-table">
          <thead>
            <tr>
              <th>نام</th>
              <th>ایمیل</th>
              <th>نقش</th>
              <th>وضعیت</th>
              <th>ایجاد</th>
              <th>عملیات</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>
                <div class="user-cell">
                  <span class="avatar-chip">{{ initials(user) }}</span>
                  <div class="user-meta">
                    <div class="name">{{ user.full_name || 'بدون نام' }}</div>
                    <div class="small-muted">ID: {{ user.id }}</div>
                  </div>
                </div>
              </td>
              <td>{{ user.email }}</td>
              <td>
                <span class="pill" :class="user.is_admin ? 'success' : ''">{{ user.is_admin ? 'ادمین' : 'کاربر' }}</span>
              </td>
              <td>
                <button class="btn-small" :class="user.is_active ? 'ghost' : ''" @click="toggleActive(user)">
                  {{ user.is_active ? 'فعال' : 'غیرفعال' }}
                </button>
              </td>
              <td>{{ formatDate(user.created_at) }}</td>
              <td class="actions">
                <button class="btn-edit" @click="openEdit(user)">✏️</button>
                <button class="btn-delete" @click="confirmDelete(user)">🗑️</button>
                <button class="btn-small" @click="toggleAdmin(user)">{{ user.is_admin ? 'حذف ادمین' : 'ارتقا ادمین' }}</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-card admin-modal">
        <div class="modal-header">
          <h2>{{ editingId ? 'ویرایش کاربر' : 'کاربر جدید' }}</h2>
          <button class="close-btn" @click="closeModal">✕</button>
        </div>
        <form class="user-form" @submit.prevent="submitForm">
          <div class="form-row">
            <div class="form-group">
              <label>نام کامل</label>
              <input v-model="form.full_name" type="text" placeholder="مثلاً علی رضایی" />
            </div>
            <div class="form-group">
              <label>ایمیل</label>
              <input v-model="form.email" type="email" required />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>رمز عبور {{ editingId ? '(در صورت نیاز به تغییر)' : '' }}</label>
              <input v-model="form.password" type="password" :required="!editingId" minlength="6" />
            </div>
            <div class="form-group">
              <label>نقش</label>
              <div class="checkbox-line">
                <input id="isAdmin" v-model="form.is_admin" type="checkbox" />
                <label for="isAdmin">ادمین باشد</label>
              </div>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>وضعیت</label>
              <div class="checkbox-line">
                <input id="isActive" v-model="form.is_active" type="checkbox" />
                <label for="isActive">فعال</label>
              </div>
            </div>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-primary">{{ editingId ? 'ذخیره' : 'ایجاد' }}</button>
            <button type="button" class="btn-secondary" @click="closeModal">انصراف</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { adminService } from '../api/services'
import { success, error } from '../composables/useToast.js'

const users = ref([])
const loading = ref(false)
const showModal = ref(false)
const editingId = ref(null)
const form = ref({
  full_name: '',
  email: '',
  password: '',
  is_admin: false,
  is_active: true
})

const adminCount = computed(() => users.value.filter(u => u.is_admin).length)
const activeCount = computed(() => users.value.filter(u => u.is_active).length)

const loadUsers = async () => {
  loading.value = true
  try {
    users.value = await adminService.getUsers()
  } catch (err) {
    console.error(err)
    notifyError('خطا در بارگذاری کاربران')
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  editingId.value = null
  form.value = { full_name: '', email: '', password: '', is_admin: false, is_active: true }
  showModal.value = true
}

const openEdit = (user) => {
  editingId.value = user.id
  form.value = {
    full_name: user.full_name,
    email: user.email,
    password: '',
    is_admin: user.is_admin,
    is_active: user.is_active
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const submitForm = async () => {
  try {
    if (editingId.value) {
      await adminService.updateUser(editingId.value, { ...form.value, password: form.value.password || undefined })
      notifySuccess('کاربر بروزرسانی شد')
    } else {
      await adminService.createUser(form.value)
      notifySuccess('کاربر ایجاد شد')
    }
    closeModal()
    await loadUsers()
  } catch (err) {
    notifyError(err.response?.data?.detail || 'عملیات ناموفق')
  }
}

const confirmDelete = async (user) => {
  if (!confirm(`حذف ${user.email}؟`)) return
  try {
    await adminService.deleteUser(user.id)
    notifySuccess('کاربر حذف شد')
    await loadUsers()
  } catch (err) {
    notifyError(err.response?.data?.detail || 'عملیات ناموفق')
  }
}

const toggleActive = async (user) => {
  try {
    await adminService.updateUser(user.id, { is_active: !user.is_active })
    notifySuccess('وضعیت به‌روز شد')
    await loadUsers()
  } catch (err) {
    notifyError(err.response?.data?.detail || 'عملیات ناموفق')
  }
}

const toggleAdmin = async (user) => {
  try {
    await adminService.updateUser(user.id, { is_admin: !user.is_admin })
    notifySuccess('نقش به‌روز شد')
    await loadUsers()
  } catch (err) {
    notifyError(err.response?.data?.detail || 'عملیات ناموفق')
  }
}

const initials = (user) => {
  if (user.full_name) {
    return user.full_name.split(' ').map(p => p[0]).join('').slice(0, 2).toUpperCase()
  }
  return user.email ? user.email[0].toUpperCase() : '؟'
}

const formatDate = (date) => {
  if (!date) return '-'
  try {
    return new Date(date).toLocaleDateString('fa-IR')
  } catch (e) {
    return date
  }
}

onMounted(loadUsers)

const notifySuccess = (message) => {
  try { success(message) } catch (err) { console.error(message, err) }
}

const notifyError = (message) => {
  try { error(message) } catch (err) { console.error(message, err) }
}
</script>

<style scoped>
.admin-users { display: flex; flex-direction: column; gap: 1.5rem; }
.header-actions { display: flex; gap: 0.75rem; }
.users-table { width: 100%; border-collapse: collapse; }
.users-table th, .users-table td { padding: 0.9rem 0.75rem; text-align: right; border-bottom: 1px solid rgba(226,232,240,0.9); }
.users-table th { color: #0f172a; font-weight: 800; background: rgba(102,126,234,0.08); }
.user-cell { display: flex; align-items: center; gap: 0.65rem; }
.avatar-chip { width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, #eef2ff, #e0e7ff); color: #312e81; display: inline-flex; align-items: center; justify-content: center; font-weight: 800; box-shadow: 0 6px 14px rgba(102,126,234,0.2); }
.user-meta .name { font-weight: 700; color: #0f172a; }
.small-muted { color: #9ca3af; font-size: 0.85rem; }
.actions { display: flex; gap: 0.4rem; align-items: center; }
.user-form { padding: 1.25rem 1.5rem 1.5rem; display: flex; flex-direction: column; gap: 1rem; }
.checkbox-line { display: flex; align-items: center; gap: 0.5rem; font-weight: 700; color: #374151; }
.checkbox-line input { width: 18px; height: 18px; }
</style>
