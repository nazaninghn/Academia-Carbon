# Quick Start Guide

## 🚀 Getting Started

### 1. Start the Server

```bash
.\venv\Scripts\activate
python manage.py runserver
```

### 2. Open Your Browser

Visit: **http://127.0.0.1:8000**

The site will automatically redirect to English version.

### 3. Available URLs

- **English**: http://127.0.0.1:8000/en/
- **Turkish**: http://127.0.0.1:8000/tr/
- **Admin Panel**: http://127.0.0.1:8000/en/admin

### 4. Admin Credentials

- **Username**: `admin`
- **Password**: `admin123`

## 🌐 Language Switching

Use the language dropdown in the top-right corner of the navigation bar to switch between English and Turkish.

## 📊 Features

1. **Global Emissions Chart**: View worldwide GHG emissions trends
2. **Country Selection**: Choose any country to see detailed data
3. **Interactive Charts**: 
   - CO2 emissions bar chart
   - Greenhouse gas comparison (doughnut chart)
   - Total emissions over time (line chart)

## 🔧 Common Commands

### Update Country Names
```bash
python manage.py load_sample_data
```

### Create New Translations
```bash
django-admin makemessages -l tr --ignore=venv
django-admin compilemessages --ignore=venv
```

### Create Superuser
```bash
python manage.py createsuperuser
```

## 📝 Adding New Countries

Via Admin Panel:
1. Go to http://127.0.0.1:8000/en/admin
2. Login with admin credentials
3. Click "Countries" → "Add Country"
4. Fill in name and code
5. Add emission data under "Emission data"

Via Django Shell:
```python
python manage.py shell

from ghg.models import Country, EmissionData

# Create country
country = Country.objects.create(name='Spain', code='ESP')

# Add emission data
EmissionData.objects.create(
    country=country,
    year=2023,
    co2_emissions=250,
    methane_emissions=60,
    nitrous_oxide=30,
    total_ghg=340
)
```

## 🎨 Customization

### Change Colors
Edit `static/css/style.css` - look for the gradient colors in `.hero-section`

### Modify Charts
Edit `static/js/charts.js` - customize chart types, colors, and options

### Add New Languages
1. Update `LANGUAGES` in `carbon_tracker/settings.py`
2. Run `django-admin makemessages -l <lang_code> --ignore=venv`
3. Edit `locale/<lang_code>/LC_MESSAGES/django.po`
4. Run `django-admin compilemessages --ignore=venv`
5. Restart server

## 🐛 Troubleshooting

**Problem**: Page shows template errors
- **Solution**: Make sure you compiled translations with `compilemessages`

**Problem**: Charts not loading
- **Solution**: Check browser console for JavaScript errors

**Problem**: Language not switching
- **Solution**: Clear browser cache and cookies

**Problem**: Admin panel not accessible
- **Solution**: Make sure you're using the correct URL with language prefix (e.g., `/en/admin`)

## 📚 Documentation

- Full README: `README.md`
- Multilingual Guide: `MULTILINGUAL.md`
- Django Documentation: https://docs.djangoproject.com/

---

**Need Help?** Check the documentation files or Django's official documentation.
