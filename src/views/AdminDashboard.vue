<template>
  <div class="admin-page admin-dashboard">
    <div class="admin-section-header">
      <div>
        <div class="eyebrow">📊 داشبورد</div>
        <h2>مرور سریع محتوا و ترافیک</h2>
        <p class="muted">هم‌راستا با سبک جدید سایت و افکت‌های شیشه‌ای</p>
        <div class="meta-chips">
          <span class="chip">بازدید کل {{ visitSummary.total_visits }}</span>
          <span class="chip subtle">IP یکتا {{ visitSummary.unique_ips }}</span>
          <span class="chip subtle">امروز {{ visitSummary.today_visits }}</span>
        </div>
      </div>
      <div class="header-actions">
        <router-link to="/admin/reports" class="btn-primary ghost">گزارش پیشرفته</router-link>
      </div>
    </div>

    <div class="card-grid stat-grid">
      <div class="card glass-card stat-tile" v-for="item in statTiles" :key="item.label">
        <div class="stat-icon">{{ item.icon }}</div>
        <div class="stat-text">
          <p class="muted">{{ item.label }}</p>
          <div class="stat-number">{{ item.value }}</div>
        </div>
        <span v-if="item.badge" class="badge">{{ item.badge }}</span>
      </div>
    </div>

    <div class="panel quick-actions">
      <div class="panel-header">
        <h3>عملیات سریع</h3>
        <span class="muted">افزودن محتوای تازه</span>
      </div>
      <div class="actions-grid">
        <router-link to="/admin/articles" class="action-button">➕ مقاله جدید</router-link>
        <router-link to="/admin/gallery" class="action-button">➕ آیتم گالری</router-link>
        <router-link to="/admin/testimonials" class="action-button">➕ نظر مشتری</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { adminService } from '../api/services'

const stats = ref({
  articles: 0,
  gallery: 0,
  testimonials: 0,
  contacts: 0,
  sliders: 0,
  certificates: 0,
  services: 0,
  unread_contacts: 0,
  pending_testimonials: 0,
  visits: {
    total: 0,
    today: 0,
    last7: 0,
    last30: 0,
    unique_ips: 0
  }
})

const visitSummary = ref({
  total_visits: 0,
  unique_ips: 0,
  today_visits: 0,
  last7_visits: 0,
  last30_visits: 0,
  per_day: []
})

onMounted(async () => {
  try {
    stats.value = await adminService.getDashboardStats()
    visitSummary.value = await adminService.getVisitSummary()
  } catch (error) {
    console.error('Failed to fetch dashboard stats:', error)
  }
})

const statTiles = computed(() => ([
  { icon: '📝', label: 'مقالات', value: stats.value.articles },
  { icon: '🎨', label: 'گالری', value: stats.value.gallery },
  { icon: '⭐', label: 'نظرات', value: stats.value.testimonials },
  { icon: '📧', label: 'پیام‌های خوانده‌نشده', value: stats.value.unread_contacts, badge: 'اهم' },
  { icon: '✅', label: 'نظرات در انتظار', value: stats.value.pending_testimonials },
  { icon: '📞', label: 'کل پیام‌ها', value: stats.value.contacts },
  { icon: '🎬', label: 'اسلایدرها', value: stats.value.sliders },
  { icon: '📜', label: 'گواهینامه‌ها', value: stats.value.certificates },
  { icon: '👁️', label: 'کل بازدید', value: visitSummary.value.total_visits },
  { icon: '📅', label: 'امروز', value: visitSummary.value.today_visits },
  { icon: '🗓️', label: '۷ روز اخیر', value: visitSummary.value.last7_visits },
  { icon: '🌐', label: 'IP یکتا', value: visitSummary.value.unique_ips }
]))
</script>
<style scoped>
.admin-dashboard { display: flex; flex-direction: column; gap: 1.5rem; }
.stat-grid { grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); }
.stat-tile { display: flex; align-items: center; gap: 1rem; padding: 1.25rem; position: relative; }
.stat-icon { font-size: 2rem; line-height: 1; }
.stat-text { flex: 1; }
.stat-number { font-size: 1.7rem; font-weight: 800; color: #111827; margin: 0.1rem 0 0; }
.badge { position: absolute; top: 0.85rem; left: 0.85rem; }

.quick-actions { margin-top: 0.5rem; }
.actions-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }
.action-button { padding: 1rem; background: linear-gradient(135deg, var(--admin-primary-start), var(--admin-primary-end)); color: #fff; text-decoration: none; border-radius: var(--admin-radius-sm); text-align: center; font-weight: 700; transition: transform 0.2s ease, box-shadow 0.25s ease; box-shadow: 0 12px 24px rgba(102,126,234,0.25); }
.action-button:hover { transform: translateY(-2px); box-shadow: var(--admin-glow); }

@media (max-width: 768px) {
  .stat-grid { grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); }
}
</style>
