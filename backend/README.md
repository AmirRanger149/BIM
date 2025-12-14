# 🚀 BIM Backend API - FastAPI

بک‌اند قدرتمند و کامل برای پروژه BIM Landing Page با استفاده از FastAPI.

## ✨ ویژگی‌ها

- ✅ **RESTful API** کامل با FastAPI
- ✅ **Authentication & Authorization** با JWT
- ✅ **SQLAlchemy ORM** برای مدیریت دیتابیس
- ✅ **Pydantic Validation** برای اعتبارسنجی داده‌ها
- ✅ **CORS Support** برای اتصال فرانت‌اند
- ✅ **Auto Documentation** با Swagger UI و ReDoc
- ✅ **Pagination** برای تمام لیست‌ها
- ✅ **Search & Filter** برای مقالات و گالری
- ✅ **Sample Data** برای تست سریع

## 📁 ساختار پروژه

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py           # تنظیمات برنامه
│   ├── database.py         # تنظیمات دیتابیس
│   ├── models.py           # مدل‌های SQLAlchemy
│   ├── schemas.py          # Pydantic schemas
│   ├── auth.py             # Authentication logic
│   └── routes/
│       ├── __init__.py
│       ├── auth_routes.py  # روت‌های احراز هویت
│       ├── articles.py     # روت‌های مقالات
│       ├── gallery.py      # روت‌های گالری
│       └── other.py        # سایر روت‌ها
├── main.py                 # فایل اصلی برنامه
├── requirements.txt        # Dependencies
├── .env.example            # نمونه environment variables
└── README.md               # این فایل
```

## 🔧 نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.8 یا بالاتر
- pip (Python package manager)

### مرحله 1: ایجاد Virtual Environment

```bash
cd backend
python -m venv venv

# فعال‌سازی در لینوکس/Mac:
source venv/bin/activate

# فعال‌سازی در ویندوز:
venv\Scripts\activate
```

### مرحله 2: نصب Dependencies

```bash
pip install -r requirements.txt
```

### مرحله 3: تنظیم Environment Variables

```bash
cp .env.example .env
```

سپس فایل `.env` را ویرایش کنید:

```env
# Database
DATABASE_URL=sqlite:///./bim.db

# Security
SECRET_KEY=your-secret-key-change-this-in-production-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
FRONTEND_URL=http://localhost:3000

# Admin User
ADMIN_EMAIL=admin@bim.com
ADMIN_PASSWORD=admin123
```

### مرحله 4: اجرای برنامه

```bash
# Development mode با auto-reload
uvicorn main:app --reload --port 8000

# یا
python main.py
```

برنامه روی http://localhost:8000 اجرا می‌شود.

## 📚 مستندات API

بعد از اجرای برنامه، می‌توانید مستندات API را در این آدرس‌ها ببینید:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentication

### ثبت‌نام کاربر جدید

```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "نام کاربر"
}
```

### ورود

```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin@bim.com&password=admin123
```

پاسخ:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### استفاده از Token

برای endpoint هایی که نیاز به احراز هویت دارند:

```http
GET /api/auth/me
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## 📡 API Endpoints

### Articles (مقالات)

```http
GET    /api/articles              # لیست مقالات (با pagination, filter, search)
GET    /api/articles/{id}         # دریافت یک مقاله
POST   /api/articles              # ایجاد مقاله (ادمین)
PUT    /api/articles/{id}         # بروزرسانی مقاله (ادمین)
DELETE /api/articles/{id}         # حذف مقاله (ادمین)
GET    /api/articles/categories/list  # لیست دسته‌بندی‌ها
```

**مثال - دریافت مقالات:**
```http
GET /api/articles?category=برنامه‌نویسی&search=vue&page=1&limit=10&sort=latest
```

### Gallery (گالری)

```http
GET    /api/gallery               # لیست پروژه‌ها
GET    /api/gallery/{id}          # دریافت یک پروژه
POST   /api/gallery               # ایجاد پروژه (ادمین)
PUT    /api/gallery/{id}          # بروزرسانی پروژه (ادمین)
DELETE /api/gallery/{id}          # حذف پروژه (ادمین)
GET    /api/gallery/categories/list  # لیست دسته‌بندی‌ها
```

### Testimonials (نظرات)

```http
GET    /api/testimonials          # دریافت نظرات تایید شده
POST   /api/testimonials          # ثبت نظر جدید
PUT    /api/testimonials/{id}/approve  # تایید نظر (ادمین)
```

### Certificates (گواهینامه‌ها)

```http
GET    /api/certificates          # دریافت گواهینامه‌ها
POST   /api/certificates          # ایجاد گواهینامه (ادمین)
```

### Statistics (آمار)

```http
GET    /api/statistics            # دریافت آمار
POST   /api/statistics            # ایجاد آمار (ادمین)
PUT    /api/statistics/{id}       # بروزرسانی آمار (ادمین)
```

### Contact (تماس)

```http
POST   /api/contact               # ارسال فرم تماس
GET    /api/contact/messages      # دریافت پیام‌ها (ادمین)
PUT    /api/contact/{id}/read     # علامت‌گذاری خوانده شده (ادمین)
```

### Newsletter (خبرنامه)

```http
POST   /api/newsletter/subscribe  # ثبت‌نام در خبرنامه
GET    /api/newsletter/subscribers  # لیست مشترکین (ادمین)
```

## 📊 مدل‌های دیتابیس

### Article (مقاله)
- title, excerpt, full_content
- category, icon, gradient
- author, author_avatar, author_role
- views, read_time, featured
- tags (JSON array)
- created_at, updated_at

### GalleryItem (پروژه)
- title, description
- icon, gradient
- category, category_color
- date, duration
- views, comments
- technologies (JSON array)

### Testimonial (نظر)
- name, role, avatar
- text, rating
- date, project
- approved (نیاز به تایید ادمین)

### Certificate (گواهینامه)
- title, issuer
- date, icon, color

### Statistic (آمار)
- number, label, icon, order

### Contact (پیام تماس)
- name, email, subject, message
- read (خوانده شده یا نه)

### Newsletter (خبرنامه)
- email, active

### User (کاربر)
- email, hashed_password
- full_name
- is_active, is_admin

## 🔒 نقش‌ها و دسترسی‌ها

### Public (عمومی)
- دریافت لیست و جزئیات مقالات
- دریافت لیست و جزئیات گالری
- دریافت نظرات تایید شده
- دریافت گواهینامه‌ها و آمار
- ارسال فرم تماس
- ثبت نظر جدید (نیاز به تایید)
- ثبت‌نام در خبرنامه

### Admin (ادمین)
- تمام دسترسی‌های public
- ایجاد، ویرایش و حذف مقالات
- ایجاد، ویرایش و حذف پروژه‌های گالری
- تایید نظرات کاربران
- مدیریت گواهینامه‌ها و آمار
- مشاهده پیام‌های تماس
- مشاهده لیست مشترکین خبرنامه

## 🧪 تست API

### با curl:

```bash
# دریافت مقالات
curl http://localhost:8000/api/articles

# ورود
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@bim.com&password=admin123"

# ایجاد مقاله (با token)
curl -X POST "http://localhost:8000/api/articles" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "مقاله جدید",
    "excerpt": "خلاصه مقاله",
    "category": "برنامه‌نویسی",
    "author": "نویسنده"
  }'
```

### با Python:

```python
import requests

# دریافت مقالات
response = requests.get("http://localhost:8000/api/articles")
print(response.json())

# ورود
login_data = {
    "username": "admin@bim.com",
    "password": "admin123"
}
response = requests.post(
    "http://localhost:8000/api/auth/login",
    data=login_data
)
token = response.json()["access_token"]

# ایجاد مقاله
headers = {"Authorization": f"Bearer {token}"}
article_data = {
    "title": "مقاله جدید",
    "excerpt": "خلاصه",
    "category": "برنامه‌نویسی",
    "author": "نویسنده"
}
response = requests.post(
    "http://localhost:8000/api/articles",
    json=article_data,
    headers=headers
)
```

## 🗄️ تغییر دیتابیس

### استفاده از PostgreSQL:

1. نصب PostgreSQL و ایجاد دیتابیس:
```sql
CREATE DATABASE bim_db;
```

2. تغییر DATABASE_URL در `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/bim_db
```

3. نصب psycopg2:
```bash
pip install psycopg2-binary
```

### استفاده از MySQL:

```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/bim_db
```

```bash
pip install pymysql
```

## 🚀 Deploy در Production

### 1. تغییرات ضروری:

**در `.env`:**
```env
DEBUG=False
SECRET_KEY=generate-a-strong-random-secret-key-here
DATABASE_URL=postgresql://user:pass@host:5432/db
FRONTEND_URL=https://yourdomain.com
```

### 2. با Docker:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. با Gunicorn:

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📝 نکات مهم

1. **امنیت:**
   - حتما `SECRET_KEY` را در production تغییر دهید
   - از HTTPS استفاده کنید
   - رمز عبور ادمین را تغییر دهید

2. **Performance:**
   - برای production از PostgreSQL استفاده کنید
   - Connection pooling را فعال کنید
   - Caching را پیاده‌سازی کنید

3. **Monitoring:**
   - از ابزارهایی مثل Sentry برای error tracking استفاده کنید
   - Log ها را نگه دارید

## 🤝 مشارکت

برای مشارکت در پروژه:
1. Fork کنید
2. برنچ جدید بسازید
3. تغییرات را commit کنید
4. Pull Request بزنید

## 📄 لایسنس

MIT License

## 💬 پشتیبانی

برای سوالات و مشکلات، issue باز کنید.

---

ساخته شده با ❤️ با FastAPI
