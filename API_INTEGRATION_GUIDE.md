# راهنمای اتصال به Backend (FastAPI)

این مستند راهنمای کامل برای اتصال فرانت‌اند Vue به بک‌اند FastAPI را ارائه می‌دهد.

## 📁 ساختار فایل‌های API

```
src/
├── api/
│   ├── client.js          # Axios instance با interceptors
│   └── services.js        # تمام API service functions
├── data/
│   ├── mockArticles.js    # Mock data برای مقالات
│   ├── mockGallery.js     # Mock data برای گالری
│   └── mockData.js        # Mock data برای سایر بخش‌ها
├── composables/
│   └── useApi.js          # Composables برای مدیریت API calls
└── components/
    └── ... (کامپوننت‌های Vue)
```

## 🔧 تنظیمات اولیه

### 1. Environment Variables

فایل `.env` را در ریشه پروژه ایجاد کنید:

```env
# URL بک‌اند FastAPI
VITE_API_BASE_URL=http://localhost:8000

# Timeout برای درخواست‌ها (میلی‌ثانیه)
VITE_API_TIMEOUT=30000

# استفاده از Mock Data یا API واقعی
VITE_USE_MOCK_DATA=true   # برای development
# VITE_USE_MOCK_DATA=false # برای production
```

**نکته مهم:** فایل `.env` در `.gitignore` است و commit نمی‌شود.

### 2. نصب Dependencies

```bash
npm install axios
```

## 📡 API Endpoints مورد نیاز در FastAPI

بک‌اند FastAPI شما باید این endpointها را پیاده‌سازی کند:

### Articles (مقالات)
- `GET /api/articles` - دریافت لیست مقالات
  - Query params: `category`, `search`, `sort`, `page`, `limit`
- `GET /api/articles/{id}` - دریافت یک مقاله
- `POST /api/articles` - ایجاد مقاله جدید
- `PUT /api/articles/{id}` - بروزرسانی مقاله
- `DELETE /api/articles/{id}` - حذف مقاله

### Gallery (گالری)
- `GET /api/gallery` - دریافت لیست پروژه‌ها
  - Query params: `category`, `search`, `page`, `limit`
- `GET /api/gallery/{id}` - دریافت یک پروژه

### Testimonials (نظرات)
- `GET /api/testimonials` - دریافت نظرات
- `POST /api/testimonials` - ثبت نظر جدید

### Certificates (گواهینامه‌ها)
- `GET /api/certificates` - دریافت گواهینامه‌ها

### Statistics (آمار)
- `GET /api/statistics` - دریافت آمار سایت

### Contact (تماس)
- `POST /api/contact` - ارسال فرم تماس

### Newsletter (خبرنامه)
- `POST /api/newsletter/subscribe` - ثبت‌نام در خبرنامه

## 🎯 نحوه استفاده

### روش 1: استفاده مستقیم از Services

```vue
<script setup>
import { ref, onMounted } from 'vue'
import { getArticles } from '@/api/services'

const articles = ref([])
const loading = ref(false)
const error = ref(null)

onMounted(async () => {
  loading.value = true
  try {
    const response = await getArticles({ 
      category: 'برنامه‌نویسی',
      page: 1,
      limit: 10
    })
    articles.value = response.data
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
})
</script>
```

### روش 2: استفاده از Composable (توصیه می‌شود)

```vue
<script setup>
import { useApi } from '@/composables/useApi'
import { getArticles } from '@/api/services'

// با immediate: true (پیش‌فرض) بلافاصله داده را می‌گیرد
const { data, loading, error, refresh } = useApi(() => getArticles())

// یا با پارامترها:
const { data: filteredData } = useApi(() => 
  getArticles({ category: 'طراحی' })
)
</script>

<template>
  <div>
    <div v-if="loading">در حال بارگذاری...</div>
    <div v-else-if="error">خطا: {{ error }}</div>
    <div v-else>
      <article v-for="article in data" :key="article.id">
        {{ article.title }}
      </article>
    </div>
    <button @click="refresh">بارگذاری مجدد</button>
  </div>
</template>
```

### روش 3: استفاده از Pagination Composable

```vue
<script setup>
import { usePagination } from '@/composables/useApi'
import { getArticles } from '@/api/services'

const {
  data: articles,
  loading,
  error,
  currentPage,
  totalPages,
  nextPage,
  prevPage,
  goToPage
} = usePagination(getArticles, 12) // 12 آیتم در هر صفحه
</script>

<template>
  <div>
    <div v-if="loading">در حال بارگذاری...</div>
    <div v-else>
      <div v-for="article in articles" :key="article.id">
        {{ article.title }}
      </div>
      
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">قبلی</button>
        <span>صفحه {{ currentPage }} از {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">بعدی</button>
      </div>
    </div>
  </div>
</template>
```

### روش 4: استفاده از Form Composable

```vue
<script setup>
import { ref } from 'vue'
import { useForm } from '@/composables/useApi'
import { sendContactForm } from '@/api/services'

const formData = ref({
  name: '',
  email: '',
  subject: '',
  message: ''
})

const { loading, error, success, submit, reset } = useForm(sendContactForm)

const handleSubmit = async () => {
  try {
    await submit(formData.value)
    // فرم با موفقیت ارسال شد
    formData.value = { name: '', email: '', subject: '', message: '' }
  } catch (err) {
    // خطا در ارسال
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <input v-model="formData.name" placeholder="نام" />
    <input v-model="formData.email" placeholder="ایمیل" />
    <input v-model="formData.subject" placeholder="موضوع" />
    <textarea v-model="formData.message" placeholder="پیام"></textarea>
    
    <button type="submit" :disabled="loading">
      {{ loading ? 'در حال ارسال...' : 'ارسال' }}
    </button>
    
    <div v-if="success" class="success">پیام با موفقیت ارسال شد!</div>
    <div v-if="error" class="error">{{ error }}</div>
  </form>
</template>
```

## 🔐 Authentication (احراز هویت)

اگر بک‌اند شما نیاز به authentication دارد:

### 1. ذخیره Token

```javascript
// بعد از لاگین موفق
localStorage.setItem('auth_token', response.data.token)
```

### 2. استفاده خودکار از Token

Token به‌طور خودکار در `client.js` به header درخواست‌ها اضافه می‌شود:

```javascript
// در api/client.js
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

## 🔄 تغییر از Mock به API واقعی

### مرحله 1: تنظیم environment variable
```env
VITE_USE_MOCK_DATA=false
```

### مرحله 2: اطمینان از اجرای بک‌اند
```bash
# مثال: اجرای FastAPI
cd backend/
uvicorn main:app --reload --port 8000
```

### مرحله 3: تست اتصال
```bash
# تست endpoint
curl http://localhost:8000/api/articles
```

## 📊 ساختار Response از Backend

همه endpoint ها باید response به این فرمت برگردانند:

```json
{
  "data": [...], // یا {}
  "total": 100,  // (اختیاری) برای pagination
  "message": "عملیات موفق" // (اختیاری)
}
```

برای خطاها:

```json
{
  "message": "توضیح خطا",
  "detail": "جزئیات بیشتر" // (اختیاری)
}
```

## 🚀 مثال FastAPI Backend

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# اضافه کردن CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # آدرس فرانت‌اند
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Article(BaseModel):
    id: int
    title: str
    excerpt: str
    category: str
    # ... سایر فیلدها

@app.get("/api/articles")
async def get_articles(
    category: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):
    # لاجیک دریافت مقالات از دیتابیس
    articles = []  # از دیتابیس بگیرید
    total = 100    # تعداد کل
    
    return {
        "data": articles,
        "total": total
    }

@app.get("/api/articles/{article_id}")
async def get_article(article_id: int):
    # دریافت یک مقاله
    article = None  # از دیتابیس بگیرید
    
    if not article:
        raise HTTPException(status_code=404, detail="مقاله یافت نشد")
    
    return {"data": article}

@app.post("/api/contact")
async def send_contact(contact_data: dict):
    # پردازش فرم تماس
    # ارسال ایمیل، ذخیره در دیتابیس و ...
    
    return {
        "success": True,
        "message": "پیام شما با موفقیت ارسال شد"
    }
```

## 🐛 Debugging

### مشاهده درخواست‌های API در Console

تمام خطاها در console نمایش داده می‌شوند. برای دیدن جزئیات بیشتر:

```javascript
// در api/client.js می‌توانید logging اضافه کنید
apiClient.interceptors.request.use((config) => {
  console.log('API Request:', config.method.toUpperCase(), config.url)
  return config
})

apiClient.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.config.url, response.data)
    return response
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)
```

## ✅ Checklist برای Production

- [ ] تغییر `VITE_USE_MOCK_DATA` به `false`
- [ ] تنظیم `VITE_API_BASE_URL` به آدرس سرور production
- [ ] فعال کردن HTTPS
- [ ] تنظیم CORS در backend
- [ ] پیاده‌سازی rate limiting
- [ ] اضافه کردن authentication/authorization
- [ ] تست تمام endpoint ها
- [ ] پیاده‌سازی error tracking (مثل Sentry)
- [ ] اضافه کردن retry logic برای درخواست‌های ناموفق

## 📚 منابع مفید

- [Axios Documentation](https://axios-http.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue 3 Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
