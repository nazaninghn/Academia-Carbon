# 🔒 Account Lockout Security System

## خلاصه
سیستم قفل خودکار اکانت برای جلوگیری از حملات Brute Force

---

## ⚙️ تنظیمات

### پیکربندی پیش‌فرض:
```python
MAX_LOGIN_ATTEMPTS = 5        # حداکثر تلاش ناموفق
LOCKOUT_DURATION = 30         # مدت قفل (دقیقه)
```

این تنظیمات در فایل `ghg/security.py` قابل تغییر هستند.

---

## 🎯 نحوه کار

### 1. ورود ناموفق
```
کاربر → ورود با پسورد اشتباه
       ↓
سیستم → شمارنده +1
       ↓
کاربر → پیام: "4 تلاش باقی مانده"
```

### 2. قفل شدن اکانت
```
کاربر → 5 بار ورود ناموفق
       ↓
سیستم → قفل اکانت (30 دقیقه)
       ↓
کاربر → پیام: "اکانت قفل شد، 30 دقیقه صبر کنید"
```

### 3. ورود موفق
```
کاربر → ورود با پسورد صحیح
       ↓
سیستم → ریست شمارنده
       ↓
کاربر → ورود به داشبورد
```

---

## 🔐 ویژگی‌ها

### ✅ محافظت دوگانه
- **Email-based**: قفل بر اساس ایمیل
- **IP-based**: قفل بر اساس IP address

### ✅ پیام‌های واضح
```python
# تلاش ناموفق
"⚠️ Invalid email or password. You have 3 attempts remaining."

# قفل شدن
"🔒 Account temporarily locked. Please try again in 28 minutes."
```

### ✅ Logging کامل
تمام رویدادهای امنیتی در `logs/security.log` ثبت میشه:
```
SECURITY EVENT: login_failed | Identifier: user@example.com | IP: 192.168.1.1
SECURITY EVENT: account_locked | Identifier: user@example.com | Locked for 30 minutes
```

---

## 🛠️ استفاده

### برای کاربران عادی:
هیچ کاری لازم نیست! سیستم خودکار کار میکنه.

### برای ادمین‌ها:

#### 1. چک کردن وضعیت اکانت
```python
from ghg.security import AccountLockout

# چک کردن قفل بودن
is_locked = AccountLockout.is_locked('user@example.com')

# تعداد تلاش‌های ناموفق
attempts = AccountLockout.get_failed_attempts('user@example.com')

# تلاش‌های باقی‌مانده
remaining = AccountLockout.get_attempts_remaining('user@example.com')

# زمان باقی‌مانده تا unlock (ثانیه)
time_left = AccountLockout.get_lockout_time_remaining('user@example.com')
```

#### 2. Unlock کردن دستی
```bash
# از طریق command line
python manage.py unlock_account user@example.com

# یا از طریق Python
from ghg.security import AccountLockout
AccountLockout.unlock_account('user@example.com')
```

---

## 🧪 تست

```bash
# اجرای تست‌ها
python manage.py test ghg.tests_security

# تست دستی
# 1. سعی کن 5 بار با پسورد اشتباه login کنی
# 2. باید پیام قفل شدن رو ببینی
# 3. بعد از 30 دقیقه دوباره امتحان کن
```

---

## 📊 مثال‌های واقعی

### سناریو 1: کاربر پسوردش رو یادش رفته
```
تلاش 1: ❌ "Invalid password. 4 attempts remaining"
تلاش 2: ❌ "Invalid password. 3 attempts remaining"
تلاش 3: ❌ "Invalid password. 2 attempts remaining"
تلاش 4: ✅ "Welcome back!"
→ شمارنده ریست شد
```

### سناریو 2: حمله Brute Force
```
تلاش 1-5: ❌ همه ناموفق
→ 🔒 اکانت قفل شد (30 دقیقه)
→ 📧 ایمیل به ادمین ارسال شد (اختیاری)
→ 📝 رویداد در log ثبت شد
```

### سناریو 3: ادمین unlock میکنه
```bash
$ python manage.py unlock_account hacker@example.com
✓ Successfully unlocked: hacker@example.com
```

---

## ⚠️ نکات مهم

### 1. Cache Backend
سیستم از Django Cache استفاده میکنه. مطمئن شو که cache درست کانفیگ شده:

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

### 2. Production Environment
در production از Redis یا Memcached استفاده کن:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### 3. Monitoring
لاگ‌های امنیتی رو مرتب چک کن:

```bash
tail -f logs/security.log
```

---

## 🔄 ادغام با سیستم‌های دیگر

### Email Notifications
```python
# در ghg/security.py
def lock_account(identifier):
    # ... existing code ...
    
    # Send email to admin
    from django.core.mail import send_mail
    send_mail(
        'Security Alert: Account Locked',
        f'Account {identifier} has been locked due to multiple failed login attempts.',
        'security@academiacarbon.com',
        ['admin@academiacarbon.com'],
    )
```

### Slack/Discord Notifications
```python
# ارسال نوتیفیکیشن به Slack
import requests

def notify_slack(message):
    webhook_url = 'YOUR_SLACK_WEBHOOK'
    requests.post(webhook_url, json={'text': message})
```

---

## 📈 آمار و گزارش

### تعداد اکانت‌های قفل شده امروز:
```python
# این نیاز به ذخیره در database داره
# فعلاً از cache استفاده میکنیم
```

### IP های مشکوک:
```python
# لیست IP هایی که بیش از 10 بار تلاش ناموفق داشتن
```

---

## 🚀 بهبودهای آینده

1. ✅ **CAPTCHA**: اضافه کردن CAPTCHA بعد از 3 تلاش ناموفق
2. ✅ **2FA**: احراز هویت دو مرحله‌ای
3. ✅ **Email Verification**: تایید ایمیل قبل از فعال شدن اکانت
4. ✅ **IP Whitelist**: لیست IP های مجاز
5. ✅ **Geolocation**: بلاک کردن کشورهای خاص

---

## 📞 پشتیبانی

اگر مشکلی پیش اومد:
1. لاگ‌ها رو چک کن: `logs/security.log`
2. Cache رو clear کن: `python manage.py clear_cache`
3. اکانت رو unlock کن: `python manage.py unlock_account EMAIL`

---

## 📝 تاریخچه تغییرات

- **2025-01-14**: نسخه اولیه Account Lockout System
  - محافظت Email-based ✅
  - محافظت IP-based ✅
  - Logging ✅
  - Management Commands ✅
  - Tests ✅
