from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-dev&h09slzzbp!j(f^_lsen+afmt_&cnl96uus15mqnjc68)60'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'HotelApp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'HotelManagementSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'HotelManagementSystem.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  'Project_hotel',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# USTAWIENIA JĘZYKOWE I REGIONALNE
LANGUAGE_CODE = 'pl'
TIME_ZONE = 'Europe/Warsaw'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('pl', _('Polish')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# USTAWIENIA PLIKÓW STATYCZNYCH
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/Media')
MEDIA_URL = '/Media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/'

# USTAWIENIA PANELU JAZZMIN
JAZZMIN_SETTINGS = {
    "site_title": "Aladu Admin",
    "site_header": "Aladu Hotel",
    "site_brand": "Aladu Hotel",
    "welcome_sign": "Witaj w panelu zarządzania hotelem Aladu",

    "topmenu_links": [
        {"name": "Wróć na stronę główną", "url": "/", "new_window": False},
    ],
    "custom_links": {
        "Hotelapp": [{
            "name": "WYLOGUJ I WRÓĆ",
            "url": "/wyloguj/",
            "icon": "fas fa-sign-out-alt",
        }]
    },
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "HotelApp.Add_Room": "fas fa-bed",
        "HotelApp.Add_Employee": "fas fa-user-tie",
        "HotelApp.Online_Booking": "fas fa-calendar-check",
    },
}