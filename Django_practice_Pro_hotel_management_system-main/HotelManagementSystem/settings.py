from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-dev&h09slzzbp!j(f^_lsen+afmt_&cnl96uus15mqnjc68)60',
)
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'HotelApp.apps.HotelappConfig',
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
                'HotelApp.context_processors.asset_version',
                'HotelApp.context_processors.hotel_roles',
            ],
        },
    },
]

WSGI_APPLICATION = 'HotelManagementSystem.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

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

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = reverse_lazy('StaffPanel')
LOGOUT_REDIRECT_URL = reverse_lazy('Home')

JAZZMIN_SETTINGS = {
    "site_title": "Hotel Aladu — Panel",
    "site_header": "Hotel Aladu",
    "site_brand": "Hotel Aladu",
    "site_logo": None,
    "site_logo_classes": "",
    "site_icon": None,
    "welcome_sign": "Witaj w panelu zarządzania hotelem Aladu",
    "copyright": "Hotel Aladu",
    "search_model": ["HotelApp.Online_Booking", "auth.User"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Strona hotelu", "url": "/", "new_window": True, "icon": "fas fa-hotel"},
        {"name": "Rezerwacje", "url": "admin:HotelApp_online_booking_changelist", "icon": "fas fa-calendar-check"},
    ],
    "usermenu_links": [
        {"name": "Strona publiczna", "url": "/", "icon": "fas fa-globe"},
        {"name": "Wyloguj", "url": "admin:logout", "icon": "fas fa-sign-out-alt"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["HotelApp", "auth"],
    "custom_links": {
        "hotelapp": [
            {
                "name": "Nowa rezerwacja (strona)",
                "url": "/OnlineBooking/",
                "icon": "fas fa-plus-circle",
                "permissions": ["HotelApp.view_online_booking"],
            },
        ],
    },
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "HotelApp": "fas fa-hotel",
        "HotelApp.online_booking": "fas fa-calendar-check",
        "HotelApp.offline_booking": "fas fa-clipboard-list",
        "HotelApp.add_room": "fas fa-bed",
        "HotelApp.add_employee": "fas fa-user-tie",
        "HotelApp.add_salarys": "fas fa-money-bill-wave",
    },
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": "admin/css/aladu-admin.css",
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "HotelApp.online_booking": "collapsible",
        "HotelApp.add_room": "horizontal_tabs",
    },
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": False,
    "accent": "accent-warning",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "flatly",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-warning",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}
