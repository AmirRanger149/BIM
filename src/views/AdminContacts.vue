<template>
  <div class="admin-contacts admin-page">
    <div class="admin-section-header">
      <div>
        <div class="eyebrow">📧 پیام‌ها</div>
        <h2>صندوق ورودی مخاطبان</h2>
        <p class="muted">نمایش سریع پیام‌های جدید و وضعیت خوانده‌نشده</p>
        <div class="meta-chips">
          <span class="chip">{{ contacts.length }} پیام</span>
          <span class="chip subtle">خوانده‌نشده {{ unreadCount }}</span>
        </div>
      </div>
    </div>

    <!-- لیست پیام‌ها -->
    <div class="panel">
      <div v-if="loading" class="loading">در حال بارگذاری...</div>
      <div v-else-if="contacts.length === 0" class="empty">
        <p>هیچ پیامی یافت نشد</p>
      </div>
      <div v-else>
        <div class="contacts-container scroll-area">
          <div 
            v-for="contact in contacts" 
            :key="contact.id" 
            class="contact-card"
            :class="{ unread: !contact.read }"
            @click="selectedContact = contact"
          >
            <div class="contact-header">
              <div class="contact-name">{{ contact.name }}</div>
              <div v-if="!contact.read" class="unread-badge">جدید</div>
            </div>
            <div class="contact-email">{{ contact.email }}</div>
            <div class="contact-subject">{{ contact.subject }}</div>
            <div class="contact-date">{{ formatDate(contact.created_at) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- جزئیات پیام -->
    <div v-if="selectedContact" class="modal-overlay" @click.self="selectedContact = null">
      <div class="modal-card admin-modal">
        <div class="modal-header">
          <h2>{{ selectedContact.subject }}</h2>
          <button @click="selectedContact = null" class="close-btn">✕</button>
        </div>
        <div class="contact-details">
          <div class="detail-section">
            <h3>از طرف:</h3>
            <p><strong>{{ selectedContact.name }}</strong></p>
            <p>{{ selectedContact.email }}</p>
          </div>

          <div class="detail-section">
            <h3>موضوع:</h3>
            <p>{{ selectedContact.subject }}</p>
          </div>

          <div class="detail-section">
            <h3>پیام:</h3>
            <p class="message-text">{{ selectedContact.message }}</p>
          </div>

          <div class="detail-section">
            <h3>تاریخ ارسال:</h3>
            <p>{{ formatFullDate(selectedContact.created_at) }}</p>
          </div>

          <div class="modal-actions">
            <button 
              v-if="!selectedContact.read"
              @click="markAsRead(selectedContact.id)"
              class="btn-primary"
            >
              ✓ علامت‌گذاری به عنوان خوانده شده
            </button>
            <button @click="deleteContact(selectedContact.id)" class="btn-delete">
              🗑️ حذف پیام
            </button>
            <button @click="selectedContact = null" class="btn-secondary">
              بستن
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { adminService } from '../api/services'

const contacts = ref([])
const selectedContact = ref(null)
const loading = ref(false)

const unreadCount = computed(() => {
  return contacts.value.filter(c => !c.read).length
})

const loadContacts = async () => {
  loading.value = true
  try {
    contacts.value = await adminService.getContacts()
  } catch (error) {
    console.error('Failed to load contacts:', error)
    notifyError('خطا در بارگذاری پیام‌ها')
  } finally {
    loading.value = false
  }
}

const markAsRead = async (id) => {
  try {
    await adminService.markContactRead(id)
    selectedContact.value.read = true
    await loadContacts()
    notifySuccess('پیام به عنوان خوانده شده علامت‌گذاری شد')
  } catch (error) {
    notifyError(error.response?.data?.detail || 'عملیات ناموفق')
  }
}

const deleteContact = async (id) => {
  if (!confirm('آیا از حذف این پیام مطمئن هستید؟')) return
  
  try {
    await adminService.deleteContact(id)
    selectedContact.value = null
    await loadContacts()
    notifySuccess('پیام حذف شد')
  } catch (error) {
    notifyError(error.response?.data?.detail || 'عملیات ناموفق')
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('fa-IR')
}

const formatFullDate = (date) => {
  return new Date(date).toLocaleString('fa-IR')
}

onMounted(() => {
  loadContacts()
})

const notifySuccess = async (message) => {
  try {
    const { success } = await import('../composables/useToast.js')
    success(message)
  } catch (err) {
    console.error(message, err)
  }
}

const notifyError = async (message) => {
  try {
    const { error } = await import('../composables/useToast.js')
    error(message)
  } catch (err) {
    console.error(message, err)
  }
}
</script>

<style scoped>
.admin-contacts {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.header-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.info-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.info-card.alert {
  border: 2px solid #fbd38d;
  background: #fffaf0;
}
<style scoped>
.admin-contacts { display: flex; flex-direction: column; gap: 1.5rem; }
.contacts-container { display: grid; gap: 0.75rem; }
.contact-card { border-radius: 12px; border: 1px solid rgba(226,232,240,0.8); padding: 1rem 1.25rem; background: rgba(255,255,255,0.9); transition: transform 0.2s ease, box-shadow 0.25s ease; }
.contact-card:hover { transform: translateY(-2px); box-shadow: var(--admin-shadow); background: rgba(255,255,255,0.95); }
.contact-card.unread { background: #fff7ed; border-left: 4px solid #fb923c; }
.contact-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem; }
.contact-name { font-weight: 700; color: #111827; }
.unread-badge { background: #fed7aa; color: #7c2d12; padding: 0.2rem 0.65rem; border-radius: 12px; font-size: 0.8rem; font-weight: 700; }
.contact-email { color: #4338ca; font-weight: 700; font-size: 0.9rem; margin-bottom: 0.15rem; }
.contact-subject { color: #4b5563; font-weight: 600; margin-bottom: 0.25rem; display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden; }
.contact-date { color: #9ca3af; font-size: 0.85rem; }
.modal-actions { display: flex; gap: 0.6rem; flex-wrap: wrap; margin-top: 1rem; }
.message-text { background: rgba(99,102,241,0.04); padding: 1rem; border-radius: 10px; border: 1px solid rgba(226,232,240,0.9); color: #111827; line-height: 1.6; }
@media (max-width: 768px) {
  .contacts-container { grid-template-columns: 1fr; }
}
</style>
  border-bottom: 1px solid #e2e8f0;
