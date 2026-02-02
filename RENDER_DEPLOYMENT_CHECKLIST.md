# 🚀 Render Deployment Checklist

## ✅ After Push to GitHub

### 1️⃣ Render Automatically Deploys
- Render pulls new code from GitHub
- Dependencies are installed
- Build is executed

### 2️⃣ ⚠️ Run Migration (Important!)

**Method 1: From Render Dashboard**
```bash
# Go to Render Dashboard
# Shell → Run Command:
python manage.py migrate
```

**Method 2: From Shell**
```bash
# If you have SSH:
python manage.py migrate
```

### 3️⃣ Load Initial Data

**Run Command:**
```bash
python manage.py load_emission_sources
```

This command:
- Creates 3 Scopes
- Adds 4 Categories
- Adds 5 Sources
- Imports 7 Emission Factors

### 4️⃣ Collect Static Files

```bash
python manage.py collectstatic --noinput
```

---

## 📋 Step by Step in Render Dashboard

### Step 1: Check Deploy
1. Go to: https://dashboard.render.com
2. Select Academia-Carbon service
3. View "Events" tab
4. Wait until "Deploy succeeded" appears

### Step 2: Run Migration
1. Open "Shell" tab
2. Run this command:
```bash
python manage.py migrate
```
3. Wait until it completes

### Step 3: Load Data
1. Keep the same Shell open
2. Run this command:
```bash
python manage.py load_emission_sources
```
3. You should see success messages

### Step 4: Test
1. Go to site: https://academia-carbon.onrender.com
2. Login with admin
3. Go to Admin Panel: `/admin/`
4. Check:
   - ✅ Emission Scopes (should be 3)
   - ✅ Emission Categories (should be 4)
   - ✅ Emission Sources (should be 5)
   - ✅ Emission Factor Data (should be 7)

---

## 🔧 If Something Goes Wrong

### Problem 1: Migration Error
```bash
# If you get migration error:
python manage.py migrate --fake-initial
```

### Problem 2: Static Files Not Showing
```bash
python manage.py collectstatic --noinput --clear
```

### Problem 3: Database is Empty
```bash
# Reload data:
python manage.py load_emission_sources
```

### Problem 4: No Admin User
```bash
# Create a new admin:
python manage.py createsuperuser
```

---

## 📊 Final Checklist

After deploy, check these items:

- [ ] Site opens
- [ ] Static files (CSS/JS) load
- [ ] You can login
- [ ] Admin Panel works
- [ ] Emission Scopes are displayed
- [ ] Emission Sources exist
- [ ] You can add new Source
- [ ] Carbon calculation works

---

## 🎯 Important Render Commands

### View Logs:
```bash
# In Render Dashboard → Logs
# or
tail -f /var/log/render.log
```

### Restart Service:
```
Render Dashboard → Manual Deploy → Deploy latest commit
```

### Clear Cache:
```bash
python manage.py clear_cache
```

---

## 💡 Important Notes

1. **Always run Migration first**
   - Before load_emission_sources
   - Before anything else

2. **Take Backup**
   - Before migration
   - From Render Dashboard → Backups

3. **Check Environment Variables**
   - DEBUG=False
   - SECRET_KEY is set
   - DATABASE_URL is correct

4. **Static Files**
   - After any CSS change
   - Run collectstatic

---

## 🚨 If Something Breaks

### Rollback to Previous Version:
```bash
# In Render Dashboard:
# Rollback → Select previous deploy
```

### Or in Git:
```bash
git revert HEAD
git push origin main
```

---

**Last Updated:** 2026-02-02  
**Version:** 2.0  
**Status:** Ready for Production ✅
