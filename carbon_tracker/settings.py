"""
Django settings for carbon_tracker project.
"""

from pathlib import Path
import os
import dj_database_url
from decouple import config
import secrets

BASE_DIR = Path(__file__).resolve().parent.parent

# =================================
# CORE SETTINGS
# =================================

DEBUG = os.environ.get("DEBUG", "True") == "True"

def generate_secret_key():
    return secrets.token_urlsafe(50)

SECRET_KEY = os.environ.get("SECRET_KEY") or generate_secret_key()

ALLOWED_HOSTS = [
    "academia-carbon.onrender.com",
    ".onrender.com",
]

if DEBUG:
    ALLOWED_HOSTS.extend(["127.0.0.1", "localhost", "testserver"])

custom_hosts = os.environ.get('ALLOWED_HOSTS', '')
if custom_hosts:
    ALLOWED_HOSTS.extend([host.strip() for host in custom_hosts.split(',') if host.strip()])

# =================================
# APPS & MIDDLEWARE
# =================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'ghg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'ghg.arcjet_simulation.ArcjetSimulatorMiddleware',
    'ghg.middleware.SecurityHeadersMiddleware',
    'ghg.middleware.RateLimitMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ghg.middleware.SecurityLoggingMiddleware',
]

ROOT_URLCONF = 'carbon_tracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'carbon_tracker.wsgi.application'

# =================================
# DATABASE
# =================================

if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
elif config('DATABASE_URL', default=None):
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# =================================
# AUTH
# =================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = [
    'ghg.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = '/en/login/'
LOGIN_REDIRECT_URL = '/en/'
LOGOUT_REDIRECT_URL = '/en/login/'

# =================================
# i18n
# =================================

LANGUAGE_CODE = 'en'
LANGUAGES = [('en', 'English'), ('tr', 'Türkçe')]
LOCALE_PATHS = [BASE_DIR / 'locale']
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# =================================
# STATIC FILES
# =================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Only add static dir if it exists
_static_dir = BASE_DIR / 'static'
if _static_dir.exists():
    STATICFILES_DIRS = [_static_dir]
else:
    STATICFILES_DIRS = []

# =================================
# CORS - Vercel Frontend
# =================================

# Vercel frontend URL (set in Render env vars)
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
]

# Add Vercel production URL
if FRONTEND_URL and FRONTEND_URL not in CORS_ALLOWED_ORIGINS:
    CORS_ALLOWED_ORIGINS.append(FRONTEND_URL)

# Add from env var
cors_origins_env = os.environ.get('CORS_ALLOWED_ORIGINS', '')
if cors_origins_env:
    for origin in cors_origins_env.split(','):
        origin = origin.strip()
        if origin and origin not in CORS_ALLOWED_ORIGINS:
            CORS_ALLOWED_ORIGINS.append(origin)

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']

CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization', 'content-type',
    'dnt', 'origin', 'user-agent', 'x-csrftoken', 'x-requested-with',
]

# =================================
# CSRF & COOKIES
# =================================

CSRF_TRUSTED_ORIGINS = [
    'https://academia-carbon.onrender.com',
]

if FRONTEND_URL:
    CSRF_TRUSTED_ORIGINS.append(FRONTEND_URL)

csrf_origins_env = os.environ.get('CSRF_TRUSTED_ORIGINS', '') or config('CSRF_TRUSTED_ORIGINS', default='')
if csrf_origins_env:
    for origin in csrf_origins_env.split(','):
        origin = origin.strip()
        if origin and origin not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(origin)

if DEBUG:
    CSRF_TRUSTED_ORIGINS.extend([
        'http://127.0.0.1:8000', 'http://localhost:8000',
        'http://127.0.0.1:3000', 'http://localhost:3000',
    ])

# Cookie settings - adapt for production vs development
if DEBUG:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_DOMAIN = None
    CSRF_COOKIE_DOMAIN = None
else:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'None'  # Cross-origin (Vercel -> Render)
    CSRF_COOKIE_SAMESITE = 'None'     # Cross-origin (Vercel -> Render)
    SESSION_COOKIE_DOMAIN = None
    CSRF_COOKIE_DOMAIN = None

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 86400  # 24 hours
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False

# =================================
# SECURITY
# =================================

SECURE_SSL_REDIRECT = not DEBUG
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
FILE_UPLOAD_PERMISSIONS = 0o644

# =================================
# LOGGING
# =================================

os.makedirs(BASE_DIR / 'logs', exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '{levelname} {asctime} {module} {message}', 'style': '{'},
        'security': {'format': 'SECURITY {levelname} {asctime} {module} {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'},
        'security_file': {'class': 'logging.FileHandler', 'filename': BASE_DIR / 'logs' / 'security.log', 'formatter': 'security'},
    },
    'root': {'handlers': ['console'], 'level': 'INFO'},
    'loggers': {
        'django': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'django.security': {'handlers': ['console', 'security_file'], 'level': 'WARNING', 'propagate': False},
        'ghg': {'handlers': ['console'], 'level': 'DEBUG' if DEBUG else 'INFO', 'propagate': False},
        'ghg.security': {'handlers': ['console', 'security_file'], 'level': 'INFO', 'propagate': False},
    },
}

# =================================
# CACHE
# =================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,
        'OPTIONS': {'MAX_ENTRIES': 1000},
    }
}

# =================================
# EMAIL
# =================================

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default='True') == 'True'
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@sustindex.com')
ADMIN_NOTIFICATION_EMAILS = config('ADMIN_NOTIFICATION_EMAILS', default='admin@sustindex.com').split(',')

# =================================
# THIRD PARTY
# =================================

RECAPTCHA_SITE_KEY = config('RECAPTCHA_SITE_KEY', default='')
RECAPTCHA_SECRET_KEY = config('RECAPTCHA_SECRET_KEY', default='')
RECAPTCHA_ENABLED = config('RECAPTCHA_ENABLED', default='False') == 'True'

SITE_NAME = 'SustIndex'
SITE_URL = config('SITE_URL', default='https://academia-carbon.onrender.com' if not DEBUG else 'http://127.0.0.1:8000')

RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'

ARCJET_KEY = config('ARCJET_KEY', default='')
ARCJET_MODE = config('ARCJET_MODE', default='SIMULATION')
ARCJET_ENABLED = config('ARCJET_ENABLED', default='True') == 'True'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'