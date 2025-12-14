# 🎉 بک‌اند کامل FastAPI آماده است!

## 🚀 راه‌اندازی سریع

### گام 1: رفتن به پوشه backend
```bash
cd backend
```

### گام 2: اجرای اسکریپت راه‌اندازی
```bash
./run.sh
```

این اسکریپت به‌طور خودکار:
- Virtual environment می‌سازد
- Dependencies را نصب می‌کند
- فایل .env را ایجاد می‌کند (در صورت نبودن)
- سرور را اجرا می‌کند

### گام 3: دسترسی به API

بعد از اجرا، به این آدرس‌ها بروید:

- **API Server**: http://localhost:8000
- **Swagger UI (مستندات تعاملی)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 اطلاعات ورود ادمین

```
Email: admin@bim.com
Password: admin123
```

## 📡 تست API

### روش 1: از طریق Swagger UI
1. به http://localhost:8000/docs بروید
2. روی "Authorize" کلیک کنید
3. ابتدا از endpoint `/api/auth/login` برای دریافت token استفاده کنید
4. Token را در قسمت Authorization وارد کنید
5. حالا می‌توانید تمام endpoint ها را تست کنید

### روش 2: با اسکریپت تست
```bash
cd backend
python test_api.py
```

### روش 3: با curl
```bash
# دریافت مقالات
curl http://localhost:8000/api/articles

# دریافت گالری
curl http://localhost:8000/api/gallery

# ورود
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@bim.com&password=admin123"
```

## 🔄 اتصال فرانت‌اند

در فرانت‌اند، فایل `.env` را ویرایش کنید:

```env
# فعلا از mock data استفاده می‌کنیم
VITE_USE_MOCK_DATA=true
VITE_API_BASE_URL=http://localhost:8000

# برای استفاده از API واقعی:
# VITE_USE_MOCK_DATA=false
```

## 📚 ساختار Endpoints

### Public (نیاز به احراز هویت ندارند)
- `GET /api/articles` - لیست مقالات
- `GET /api/articles/{id}` - جزئیات مقاله
- `GET /api/gallery` - لیست گالری
- `GET /api/gallery/{id}` - جزئیات پروژه
- `GET /api/testimonials` - نظرات تایید شده
- `GET /api/certificates` - گواهینامه‌ها
- `GET /api/statistics` - آمار
- `POST /api/contact` - ارسال فرم تماس
- `POST /api/newsletter/subscribe` - ثبت‌نام خبرنامه
- `POST /api/auth/login` - ورود
- `POST /api/auth/register` - ثبت‌نام

### Protected (نیاز به توکن ادمین)
- `POST /api/articles` - ایجاد مقاله
- `PUT /api/articles/{id}` - ویرایش مقاله
- `DELETE /api/articles/{id}` - حذف مقاله
- همین‌طور برای gallery، certificates، statistics

## 🗄️ دیتابیس

بک‌اند به‌صورت پیش‌فرض از **SQLite** استفاده می‌کند که برای development عالی است.

فایل دیتابیس: `backend/bim.db`

### تغییر به PostgreSQL:

1. نصب PostgreSQL
2. ایجاد دیتابیس:
```sql
CREATE DATABASE bim_db;
```

3. تغییر `DATABASE_URL` در `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/bim_db
```

## 📊 داده‌های نمونه

بک‌اند به‌صورت خودکار داده‌های نمونه ایجاد می‌کند:
- 3 مقاله
- 2 پروژه گالری
- 1 نظر
- 4 آمار
- 2 گواهینامه

## 🛠️ توسعه

### نصب دستی dependencies:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # در لینوکس/Mac
# یا
venv\Scripts\activate  # در ویندوز

pip install -r requirements.txt
```

### اجرای دستی سرور:
```bash
cd backend
python main.py

# یا با uvicorn:
uvicorn main:app --reload --port 8000
```

## 🐛 رفع مشکلات

### خطای "Port already in use":
```bash
# پیدا کردن process
lsof -i :8000

# یا
netstat -ano | grep 8000

# kill کردن process
kill -9 <PID>
```

### خطای import:
```bash
# مطمئن شوید در virtual environment هستید
which python  # باید به venv اشاره کند

# نصب مجدد dependencies
pip install -r requirements.txt
```

### خطای دیتابیس:
```bash
# حذف دیتابیس و ایجاد مجدد
rm bim.db
python main.py
```

## 📝 نکات مهم

1. **امنیت**: در production حتما `SECRET_KEY` و `ADMIN_PASSWORD` را تغییر دهید
2. **CORS**: اگر فرانت‌اند روی پورت دیگری است، در `config.py` اضافه کنید
3. **Logging**: تمام خطاها در console نمایش داده می‌شوند
4. **Documentation**: از Swagger UI برای تست و دیدن تمام endpoint ها استفاده کنید

## 🎯 مراحل بعدی

1. ✅ بک‌اند را اجرا کنید و تست کنید
2. ✅ از Swagger UI برای آشنایی با API استفاده کنید
3. ✅ فرانت‌اند را به بک‌اند متصل کنید (تغییر `VITE_USE_MOCK_DATA` به `false`)
4. ✅ برای production آماده‌سازی کنید

## 📞 پشتیبانی

برای سوالات، به فایل `backend/README.md` مراجعه کنید که شامل:
- مستندات کامل API
- مثال‌های کد
- راهنمای deploy
- و بیشتر...

---

**موفق باشید! 🚀**
