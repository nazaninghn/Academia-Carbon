# Architecture Overview

## System Architecture

This project uses a **decoupled architecture** with separate frontend and backend:

### Backend: Django (Port 8000)
- **Purpose**: REST API only
- **URL**: `http://127.0.0.1:8000`
- **Responsibilities**:
  - Database operations (PostgreSQL/SQLite)
  - Authentication & Authorization
  - Emission calculations
  - Data validation
  - Business logic
  - Admin panel (`/django-admin/`)

### Frontend: Next.js (Port 3001)
- **Purpose**: User Interface
- **URL**: `http://127.0.0.1:3001`
- **Responsibilities**:
  - All user-facing pages
  - React components
  - Client-side routing
  - API consumption
  - Bilingual support (EN/TR)

## How It Works

```
User Browser
     ↓
Next.js Frontend (Port 3001)
     ↓ (API calls)
Django Backend (Port 8000)
     ↓
Database
```

## Running the Application

### Start Backend (Django)
```bash
cd Academia-Carbon
python manage.py runserver
```

### Start Frontend (Next.js)
```bash
cd Academia-Carbon/frontend
npm run dev
```

### Access the Application
- **Main App**: http://127.0.0.1:3001
- **API**: http://127.0.0.1:8000/en/api/
- **Admin**: http://127.0.0.1:8000/django-admin/

## Key Features

### Unified Dashboard
- Single-page application with 7 sections:
  1. Data Collection (with inline calculations)
  2. Analysis
  3. Reporting
  4. Action Planning
  5. Settings
  6. Help & Guide
  7. Support

### API Endpoints
All API endpoints are under `/en/api/`:
- `/api/auth/login/` - User login
- `/api/auth/signup/` - User registration
- `/api/scopes/` - Get emission scopes
- `/api/categories/` - Get emission categories
- `/api/sources/` - Get emission sources
- `/api/calculate/` - Calculate emissions
- `/api/dashboard/` - Dashboard statistics
- `/api/suppliers/` - Supplier management
- And more...

## Development Notes

- **No HTML Templates**: Django no longer serves HTML pages
- **API Only**: Django is purely a REST API backend
- **Next.js Handles UI**: All user interface is in Next.js
- **Session Cookies**: Use `credentials: 'include'` in fetch calls
- **CORS Enabled**: Django allows requests from Next.js frontend

## File Structure

```
Academia-Carbon/
├── carbon_tracker/       # Django project settings
├── ghg/                  # Django app (API views, models)
├── frontend/             # Next.js application
│   ├── app/             # Next.js pages
│   ├── contexts/        # React contexts
│   └── lib/             # Utilities
├── locale/              # Translations
├── logs/                # Security logs
└── manage.py            # Django management
```

## Bilingual Support

- **Languages**: English (EN) and Turkish (TR - Istanbul dialect)
- **Implementation**: React Context API
- **Switching**: Globe icon in navbar
- **Backend**: Django i18n for API messages
- **Frontend**: Custom translation system in Next.js

## Security Features

- Arcjet simulation middleware
- Rate limiting
- CSRF protection
- Session-based authentication
- Security headers
- Logging system

## Test Credentials

- **Email**: test@test.com
- **Password**: test123
