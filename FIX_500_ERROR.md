# Fix 500 Error on Render - Step by Step

## Problem
POST requests to /en/login/ and /en/signup/ return 500 error.

## Solution

### Step 1: Run Migrations in Render Shell

Go to: **Render Dashboard → academia-carbon → Shell**

Run these commands ONE BY ONE:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

### Step 2: Check Environment Variables

Go to: **Render Dashboard → academia-carbon → Environment**

Make sure you have these:

```
DEBUG=False
SECRET_KEY=(auto-generated)
ALLOWED_HOSTS=.onrender.com,academia-carbon.onrender.com
DATABASE_URL=(auto-provided)
CSRF_TRUSTED_ORIGINS=https://academia-carbon.onrender.com
```

### Step 3: Redeploy

1. Click "Manual Deploy"
2. Select "Clear build cache & deploy"
3. Wait for deployment to complete

### Step 4: Test

After deployment, try:
1. Go to: https://academia-carbon.onrender.com/en/signup/
2. Create a new account
3. Login

## If Still Getting 500 Error

### Check Detailed Logs

In Render Dashboard → Logs, look for Python traceback.

Common errors:

**Error: "relation does not exist"**
Solution: Run migrations
```bash
python manage.py migrate --run-syncdb
```

**Error: "No module named 'ghg.backends'"**
Solution: Check that ghg/backends.py exists in your repo

**Error: "CSRF verification failed"**
Solution: Add CSRF_TRUSTED_ORIGINS to environment

### Force Fresh Deploy

1. Go to Render Dashboard
2. Click "Manual Deploy"
3. Select "Clear build cache & deploy"
4. After deploy, run in Shell:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## Create First User

After fixing 500 error, create a user:

**Option 1: Use Signup Page**
- Go to: https://academia-carbon.onrender.com/en/signup/
- Fill the form
- Create account

**Option 2: Use Shell**
```bash
python manage.py createsuperuser
```

Or:
```python
from django.contrib.auth.models import User
User.objects.create_superuser(
    username='admin@example.com',
    email='admin@example.com',
    password='YourSecurePassword'
)
```

## Success Checklist

- [ ] Migrations run successfully
- [ ] Static files collected
- [ ] Environment variables set
- [ ] Can access signup page
- [ ] Can create account
- [ ] Can login
- [ ] Dashboard loads

## Still Not Working?

Send me the Python traceback from Render Logs (the red error message).
