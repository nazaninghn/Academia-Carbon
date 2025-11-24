# ✅ چک‌لیست Deploy روی Render.com

## 📋 وضعیت فایل‌ها

### ✅ فایل‌های آماده:
- [x] `requirements.txt` - همه ماژول‌ها موجود است
- [x] `render.yaml` - تنظیمات Render
- [x] `build.sh` - اسکریپت build
- [x] `ghg/backends.py` - Custom authentication backend
- [x] `carbon_tracker/settings.py` - تنظیمات production-ready

---

## 🔧 تغییرات جدید که باید Deploy بشن

### 1. **Authentication Backend جدید**
```python
# ghg/backends.py
- امکان لاگین با ایمیل
- سازگار با production
```

### 2. **تنظیمات Settings**
```python
AUTHENTICATION_BACKENDS = [
    'ghg.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```

### 3. **Responsive Design**
- همه template‌ها responsive شدن
- Mobile-friendly
- قابلیت اسکرول در صفحات login/signup

---

## 🚀 مراحل Deploy روی Render.com

### مرحله 1: Push کردن به GitHub
```bash
git add .
git commit -m "Add email authentication and responsive design"
git push origin main
```

### مرحله 2: تنظیمات Render Dashboard
1. برو به: https://dashboard.render.com
2. سرویس `academia-carbon` رو انتخاب کن
3. روی "Manual Deploy" کلیک کن
4. منتظر بمون تا build تموم بشه

### مرحله 3: بررسی Environment Variables
مطمئن شو این متغیرها تنظیم شدن:
```
✅ SECRET_KEY (auto-generated)
✅ DEBUG = False
✅ ALLOWED_HOSTS = .onrender.com
✅ DATABASE_URL (from database)
```

### مرحله 4: ایجاد Superuser روی Render
بعد از deploy موفق:
```bash
# در Render Shell:
python manage.py createsuperuser
```

یا از طریق Render Dashboard:
1. برو به سرویس خودت
2. کلیک روی "Shell"
3. اجرا کن:
```python
from django.contrib.auth.models import User
User.objects.create_superuser('admin@example.com', 'admin@example.com', 'your-password')
```

---

## 🔍 چک کردن Deploy

### 1. بررسی Build Logs
```
✅ Installing requirements
✅ Collecting static files
✅ Running migrations
✅ Starting gunicorn
```

### 2. تست صفحات
```
✅ https://your-app.onrender.com/en/login/
✅ https://your-app.onrender.com/en/signup/
✅ https://your-app.onrender.com/en/
```

### 3. تست لاگین
- با ایمیل و پسورد لاگین کن
- مطمئن شو redirect به dashboard می‌شه
- چک کن responsive روی موبایل کار می‌کنه

---

## ⚠️ مشکلات احتمالی و راه‌حل

### مشکل 1: Static Files نمایش داده نمی‌شن
**راه‌حل:**
```bash
# در Render Shell:
python manage.py collectstatic --noinput
```

### مشکل 2: Database Migration Error
**راه‌حل:**
```bash
# در Render Shell:
python manage.py migrate --run-syncdb
```

### مشکل 3: ModuleNotFoundError
**راه‌حل:**
- چک کن `requirements.txt` کامل باشه
- Redeploy کن

### مشکل 4: ALLOWED_HOSTS Error
**راه‌حل:**
در Render Dashboard:
```
ALLOWED_HOSTS = .onrender.com,your-app.onrender.com
```

### مشکل 5: CSRF Error
**راه‌حل:**
در `settings.py` چک کن:
```python
CSRF_TRUSTED_ORIGINS = [
    'https://your-app.onrender.com',
]
```

---

## 📝 تنظیمات اضافی برای Production

### 1. اضافه کردن CSRF_TRUSTED_ORIGINS
در Render Dashboard > Environment:
```
CSRF_TRUSTED_ORIGINS = https://your-app.onrender.com
```

### 2. تنظیم SECURE Settings
این‌ها در `settings.py` فعال هستن:
```python
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

---

## 🎯 چک‌لیست نهایی قبل از Deploy

- [ ] همه تغییرات commit شدن
- [ ] Push به GitHub انجام شده
- [ ] `requirements.txt` به‌روز است
- [ ] `build.sh` قابل اجرا است (chmod +x build.sh)
- [ ] Environment variables در Render تنظیم شدن
- [ ] Database متصل است

---

## 🔐 ایجاد کاربر اول روی Render

### روش 1: از طریق Shell
```bash
# در Render Shell
python manage.py shell

# در Python Shell:
from django.contrib.auth.models import User
user = User.objects.create_user(
    username='your@email.com',
    email='your@email.com',
    password='your-secure-password',
    first_name='Your Name'
)
user.save()
```

### روش 2: از طریق Signup Page
1. برو به: `https://your-app.onrender.com/en/signup/`
2. ثبت‌نام کن
3. لاگین کن

---

## 📊 مانیتورینگ

### چک کردن Logs
در Render Dashboard:
1. برو به سرویس خودت
2. کلیک روی "Logs"
3. ببین آیا خطایی هست

### متریک‌های مهم
- Response Time
- Error Rate
- Memory Usage
- Database Connections

---

## 🆘 اگر مشکلی پیش اومد

### 1. چک کردن Logs
```bash
# در Render Dashboard > Logs
# دنبال خطاهای Python بگرد
```

### 2. تست Local
```bash
# با تنظیمات production تست کن:
DEBUG=False python manage.py runserver
```

### 3. Rollback
اگر deploy جدید مشکل داره:
- در Render Dashboard
- برو به "Deploys"
- روی deploy قبلی کلیک کن
- "Rollback to this deploy"

---

## ✅ تایید نهایی

بعد از deploy موفق، این‌ها رو تست کن:

### Desktop:
- [ ] صفحه لاگین باز می‌شه
- [ ] می‌تونی با ایمیل لاگین کنی
- [ ] Dashboard نمایش داده می‌شه
- [ ] Static files (CSS/JS) لود می‌شن

### Mobile:
- [ ] صفحه responsive است
- [ ] منوی موبایل کار می‌کنه
- [ ] فرم‌ها قابل استفاده هستن
- [ ] اسکرول کار می‌کنه

### Functionality:
- [ ] لاگین با ایمیل کار می‌کنه
- [ ] ثبت‌نام کار می‌کنه
- [ ] Dashboard data نمایش داده می‌شه
- [ ] Logout کار می‌کنه

---

## 🎉 موفقیت!

اگر همه چک‌لیست‌ها ✅ شدن، پروژه شما روی Render.com با موفقیت deploy شده!

**URL سایت شما:**
```
https://your-app.onrender.com
```

---

## 📞 پشتیبانی

اگر مشکلی داشتی:
1. Render Logs رو چک کن
2. GitHub Issues رو ببین
3. Render Community Forum

---

**آخرین به‌روزرسانی:** 2025-01-24  
**وضعیت:** ✅ آماده برای Deploy
