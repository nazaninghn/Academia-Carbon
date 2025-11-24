# 🚀 دستورات سریع Deploy به Render.com

## 📦 آماده‌سازی

### 1. چک کردن تغییرات
```bash
git status
```

### 2. اضافه کردن همه فایل‌ها
```bash
git add .
```

### 3. Commit با پیام مناسب
```bash
git commit -m "Add email authentication, responsive design, and bug fixes"
```

### 4. Push به GitHub
```bash
git push origin main
```

---

## 🔄 Deploy خودکار روی Render

بعد از push، Render به صورت خودکار:
1. تغییرات رو تشخیص می‌ده
2. Build رو شروع می‌کنه
3. Deploy می‌کنه

**زمان تقریبی:** 3-5 دقیقه

---

## 🖥️ Deploy دستی (اگر خودکار نشد)

### روش 1: از Dashboard
1. برو به: https://dashboard.render.com
2. سرویس `academia-carbon` رو انتخاب کن
3. کلیک روی "Manual Deploy" > "Deploy latest commit"

### روش 2: از CLI
```bash
# نصب Render CLI (اگر نداری)
npm install -g render-cli

# لاگین
render login

# Deploy
render deploy
```

---

## 🔍 مانیتورینگ Deploy

### دیدن Logs زنده
```bash
# در Render Dashboard:
Services > academia-carbon > Logs
```

### چک کردن وضعیت
```bash
# باید این‌ها رو ببینی:
✅ Installing requirements
✅ Collecting static files  
✅ Running migrations
✅ Starting gunicorn
✅ Deploy live
```

---

## ✅ تست بعد از Deploy

### 1. چک کردن سایت
```bash
# باز کن در مرورگر:
https://your-app.onrender.com/en/login/
```

### 2. تست لاگین
- ایمیل و پسورد وارد کن
- باید به dashboard redirect بشی

### 3. تست Responsive
- باز کن در موبایل
- چک کن منو کار می‌کنه
- اسکرول رو تست کن

---

## 🆘 اگر خطا داد

### خطای Build
```bash
# چک کن requirements.txt کامل باشه
cat requirements.txt

# اگر چیزی کم بود:
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### خطای Migration
```bash
# در Render Shell:
python manage.py migrate --run-syncdb
```

### خطای Static Files
```bash
# در Render Shell:
python manage.py collectstatic --noinput
```

---

## 🔐 ایجاد اولین کاربر

### بعد از Deploy موفق:
```bash
# در Render Dashboard > Shell:
python manage.py createsuperuser
```

یا:
```python
from django.contrib.auth.models import User
User.objects.create_superuser(
    username='admin@example.com',
    email='admin@example.com', 
    password='your-secure-password'
)
```

---

## 📝 دستورات مفید

### دیدن Environment Variables
```bash
# در Render Dashboard:
Environment > View All
```

### Restart سرویس
```bash
# در Render Dashboard:
Manual Deploy > Clear build cache & deploy
```

### دیدن Database
```bash
# در Render Dashboard:
PostgreSQL > Connect
```

---

## 🎯 چک‌لیست سریع

قبل از هر Deploy:
- [ ] `git status` - همه چیز commit شده؟
- [ ] تست local - کار می‌کنه؟
- [ ] `requirements.txt` - به‌روز است؟
- [ ] `build.sh` - قابل اجرا است؟

بعد از Deploy:
- [ ] Logs - خطایی نیست؟
- [ ] سایت - باز می‌شه؟
- [ ] لاگین - کار می‌کنه؟
- [ ] Responsive - روی موبایل خوبه؟

---

## 💡 نکات مهم

1. **اولین Deploy**: 5-10 دقیقه طول می‌کشه
2. **Deploy‌های بعدی**: 2-3 دقیقه
3. **Free Plan**: بعد از 15 دقیقه بی‌فعالیت، sleep می‌شه
4. **Wake Up**: اولین request بعد از sleep، 30 ثانیه طول می‌کشه

---

## 🔗 لینک‌های مفید

- **Dashboard**: https://dashboard.render.com
- **Docs**: https://render.com/docs
- **Status**: https://status.render.com
- **Community**: https://community.render.com

---

**آخرین به‌روزرسانی:** 2025-01-24  
**وضعیت:** ✅ آماده برای Deploy
