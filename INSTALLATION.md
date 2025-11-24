# Installation Guide

Complete installation guide for Academia Carbon.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Virtual environment (recommended)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/academia-carbon.git
cd academia-carbon
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Settings

Create a `.env` file (optional):
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

Or create a user with email:
```bash
python manage.py create_email_user admin@example.com password123 --first-name "Admin" --last-name "User"
```

### 7. Load Sample Data (Optional)

```bash
python manage.py load_sample_data
```

### 8. Run the Server

```bash
python manage.py runserver
```

### 9. Access the Application

Open your browser and go to:
```
http://127.0.0.1:8000/
```

---

## Troubleshooting

### Issue: Module not found

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Database locked

**Solution:**
```bash
python manage.py migrate --run-syncdb
```

### Issue: Static files not loading

**Solution:**
```bash
python manage.py collectstatic
```

### Issue: Port already in use

**Solution:**
```bash
python manage.py runserver 8080
```

---

## Production Deployment

### 1. Update Settings

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')
```

### 2. Use Production Database

Replace SQLite with PostgreSQL or MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'academiacarbon',
        'USER': 'dbuser',
        'PASSWORD': 'dbpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Collect Static Files

```bash
python manage.py collectstatic
```

### 4. Use Production Server

Install gunicorn:
```bash
pip install gunicorn
```

Run with gunicorn:
```bash
gunicorn carbon_tracker.wsgi:application --bind 0.0.0.0:8000
```

### 5. Configure Nginx (Optional)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/academia-carbon/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Docker Installation (Alternative)

### 1. Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "carbon_tracker.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### 2. Build and Run

```bash
docker build -t academia-carbon .
docker run -p 8000:8000 academia-carbon
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| SECRET_KEY | Django secret key | (required) |
| DEBUG | Debug mode | False |
| ALLOWED_HOSTS | Allowed hosts | localhost |
| DATABASE_URL | Database URL | sqlite:///db.sqlite3 |

---

## System Requirements

### Minimum
- CPU: 1 core
- RAM: 512 MB
- Storage: 100 MB

### Recommended
- CPU: 2 cores
- RAM: 2 GB
- Storage: 1 GB

---

## Next Steps

After installation:

1. Read the [User Guide](USER_GUIDE.md)
2. Check the [Quick Reference](QUICK_REFERENCE.md)
3. Review [Emission Factors](EMISSION_FACTORS_2025.md)
4. Explore the dashboard

---

## Support

Need help? 
- Check [Troubleshooting](#troubleshooting)
- Open an [issue](https://github.com/yourusername/academia-carbon/issues)
- Read the [documentation](.)

---

**Happy tracking!** 🌍
