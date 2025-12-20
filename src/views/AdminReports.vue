<template>
  <div class="admin-page admin-analytics">
    <div class="admin-section-header">
      <div>
        <div class="eyebrow">📈 گزارش بازدید</div>
        <h2>تحلیل ترافیک و رفتار مخاطب</h2>
        <p class="muted">داده‌های ذخیره‌شده از مقالات، گالری و سایر صفحات سایت</p>
        <div class="meta-chips">
          <span class="chip">کل: {{ summary.total_visits }}</span>
          <span class="chip subtle">IP یکتا: {{ summary.unique_ips }}</span>
          <span class="chip subtle">امروز: {{ summary.today_visits }}</span>
        </div>
      </div>
      <div class="header-actions range-switch">
        <button
          v-for="range in ranges"
          :key="range"
          class="btn-small"
          :class="{ ghost: range !== rangeDays }"
          @click="changeRange(range)"
        >
          {{ range }} روزه
        </button>
      </div>
    </div>

    <div class="card-grid analytics-cards">
      <div class="card glass-card">
        <div class="card-title">کل بازدید در بازه</div>
        <div class="metric-number">{{ report.total }}</div>
        <div class="muted">میانگین روزانه {{ avgPerDay }}</div>
      </div>
      <div class="card glass-card">
        <div class="card-title">پیک ترافیک</div>
        <div class="metric-number">{{ peakDay.count }}</div>
        <div class="muted">{{ peakDay.dayLabel }}</div>
      </div>
      <div class="card glass-card">
        <div class="card-title">مسیر طلایی</div>
        <div class="muted">{{ topPathLabel }}</div>
        <div class="mini-bar" v-if="report.top_paths.length">
          <span class="fill" :style="{ width: barWidth(report.top_paths[0].count, topPathMax) }"></span>
        </div>
      </div>
      <div class="card glass-card">
        <div class="card-title">بهترین ارجاع</div>
        <div class="muted">{{ topRefererLabel }}</div>
        <div class="mini-bar" v-if="report.top_referers.length">
          <span class="fill" :style="{ width: barWidth(report.top_referers[0].count, refererMax) }"></span>
        </div>
      </div>
    </div>

    <div class="panel analytics-panel">
      <div class="panel-header">
        <h3>روند روزانه</h3>
        <span class="muted">آخرین {{ report.range_days }} روز</span>
      </div>
      <div v-if="report.per_day.length" class="sparkline">
        <div
          v-for="(point, idx) in report.per_day"
          :key="idx"
          class="spark-bar"
          :style="{ height: barHeight(point.count) }"
        >
          <div class="bar-tooltip">{{ formatDate(point.day) }} — {{ point.count }}</div>
        </div>
      </div>
      <div v-else class="empty">داده‌ای برای نمایش نیست</div>
    </div>

    <div class="panel two-col">
      <div class="col">
        <div class="panel-header">
          <h3>مسیرهای پر بازدید</h3>
          <span class="muted">Top {{ report.top_paths.length }}</span>
        </div>
        <ul class="ranked-list">
          <li v-for="path in report.top_paths" :key="path.path">
            <div class="label">{{ path.path }}</div>
            <div class="bar">
              <span class="fill" :style="{ width: barWidth(path.count, topPathMax) }"></span>
            </div>
            <span class="count">{{ path.count }}</span>
          </li>
        </ul>
      </div>
      <div class="col">
        <div class="panel-header">
          <h3>سهم بخش‌ها</h3>
          <span class="muted">گالری / مقالات / ...</span>
        </div>
        <ul class="ranked-list compact">
          <li v-for="section in report.by_section" :key="section.section">
            <div class="label">{{ sectionLabel(section.section) }}</div>
            <div class="bar">
              <span class="fill" :style="{ width: barWidth(section.count, sectionMax) }"></span>
            </div>
            <span class="count">{{ section.count }}</span>
          </li>
        </ul>
        <div class="panel-header space-top">
          <h4>منابع ارجاع برتر</h4>
        </div>
        <ul class="ranked-list compact">
          <li v-for="ref in report.top_referers" :key="ref.referer || 'direct'">
            <div class="label">{{ ref.referer || 'مستقیم / نامشخص' }}</div>
            <div class="bar">
              <span class="fill" :style="{ width: barWidth(ref.count, refererMax) }"></span>
            </div>
            <span class="count">{{ ref.count }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { adminService } from '../api/services'

const summary = ref({
  total_visits: 0,
  unique_ips: 0,
  today_visits: 0,
  last7_visits: 0,
  last30_visits: 0,
  per_day: []
})

const report = ref({
  range_days: 30,
  total: 0,
  per_day: [],
  top_paths: [],
  by_section: [],
  top_referers: []
})

const rangeDays = ref(30)
const ranges = [7, 30, 90]
const loading = ref(false)

const topPathMax = computed(() => Math.max(...report.value.top_paths.map(p => p.count || 0), 1))
const sectionMax = computed(() => Math.max(...report.value.by_section.map(p => p.count || 0), 1))
const refererMax = computed(() => Math.max(...report.value.top_referers.map(p => p.count || 0), 1))
const perDayMax = computed(() => Math.max(...report.value.per_day.map(p => p.count || 0), 1))

const avgPerDay = computed(() => {
  if (!report.value.range_days) return 0
  return Math.round(report.value.total / report.value.range_days)
})

const peakDay = computed(() => {
  if (!report.value.per_day.length) return { count: 0, dayLabel: 'بدون داده' }
  const peak = report.value.per_day.reduce((acc, curr) => curr.count > acc.count ? curr : acc)
  return {
    count: peak.count,
    dayLabel: formatDate(peak.day)
  }
})

const topPathLabel = computed(() => {
  if (!report.value.top_paths.length) return 'داده‌ای نیست'
  return `${report.value.top_paths[0].path} · ${report.value.top_paths[0].count}`
})

const topRefererLabel = computed(() => {
  if (!report.value.top_referers.length) return 'داده‌ای نیست'
  const label = report.value.top_referers[0].referer || 'مستقیم'
  return `${label} · ${report.value.top_referers[0].count}`
})

const formatDate = (day) => {
  try {
    return new Date(day).toLocaleDateString('fa-IR')
  } catch (e) {
    return day
  }
}

const barHeight = (count) => {
  const pct = Math.round((count / perDayMax.value) * 100)
  return `${Math.max(6, pct)}%`
}

const barWidth = (count, max) => {
  if (!max) return '0%'
  const pct = Math.round((count / max) * 100)
  return `${Math.max(6, pct)}%`
}

const sectionLabel = (key) => {
  const map = {
    articles: 'مقالات',
    gallery: 'گالری',
    services: 'خدمات',
    contacts: 'تماس',
    home: 'خانه',
    other: 'سایر'
  }
  return map[key] || key
}

const fetchSummary = async () => {
  try {
    summary.value = await adminService.getVisitSummary()
  } catch (error) {
    console.error('Failed to load visit summary', error)
    notifyError('خطا در دریافت خلاصه بازدیدها')
  }
}

const fetchReport = async () => {
  loading.value = true
  try {
    const data = await adminService.getVisitReport({ days: rangeDays.value })
    report.value = data
  } catch (error) {
    console.error('Failed to load visit report', error)
    notifyError('خطا در دریافت گزارش بازدیدها')
  } finally {
    loading.value = false
  }
}

const changeRange = (days) => {
  if (rangeDays.value === days) return
  rangeDays.value = days
  fetchReport()
}

onMounted(async () => {
  await fetchSummary()
  await fetchReport()
})

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
.admin-analytics { display: flex; flex-direction: column; gap: 1.5rem; }
.range-switch { display: flex; gap: 0.5rem; flex-wrap: wrap; }

.analytics-cards .card { min-height: 140px; }
.metric-number { font-size: 2rem; font-weight: 800; margin: 0.35rem 0; color: #111827; }
.mini-bar { height: 8px; background: #e5e7eb; border-radius: 999px; overflow: hidden; }
.mini-bar .fill { display: block; height: 100%; background: linear-gradient(135deg, #0ea5e9, #06b6d4); border-radius: inherit; }

.analytics-panel { overflow: hidden; }
.sparkline { display: flex; align-items: flex-end; gap: 6px; min-height: 160px; padding: 0.5rem 0; }
.spark-bar { flex: 1; background: linear-gradient(180deg, rgba(102,126,234,0.08), rgba(102,126,234,0.45)); border-radius: 10px 10px 4px 4px; position: relative; transition: transform 0.15s ease, box-shadow 0.15s ease; }
.spark-bar:hover { transform: translateY(-4px); box-shadow: 0 10px 24px rgba(102,126,234,0.18); }
.bar-tooltip { position: absolute; inset: auto auto 110% 50%; transform: translateX(-50%); white-space: nowrap; background: #111827; color: white; padding: 0.35rem 0.65rem; border-radius: 8px; font-size: 0.75rem; opacity: 0; pointer-events: none; transition: opacity 0.15s ease; }
.spark-bar:hover .bar-tooltip { opacity: 1; }

.two-col { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.25rem; }
.col { display: flex; flex-direction: column; gap: 0.75rem; }

.ranked-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 0.75rem; }
.ranked-list li { display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 0.75rem; padding: 0.85rem 1rem; border-radius: 12px; background: rgba(255,255,255,0.85); border: 1px solid rgba(226,232,240,0.8); box-shadow: 0 4px 14px rgba(0,0,0,0.04); }
.ranked-list .label { font-weight: 700; color: #111827; }
.ranked-list .bar { height: 8px; background: #f1f5f9; border-radius: 999px; overflow: hidden; grid-column: 1 / 2; }
.ranked-list .bar .fill { display: block; height: 100%; background: linear-gradient(90deg, #0ea5e9, #06b6d4); }
.ranked-list .count { font-weight: 800; color: #4b5563; }
.ranked-list.compact li { padding: 0.65rem 0.75rem; }

.space-top { margin-top: 0.5rem; }

@media (max-width: 768px) {
  .analytics-cards { grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
}
</style>
