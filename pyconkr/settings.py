"""
Django settings for pyconkr project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%fpc9qokbuc2vfl6t9gq&hpk2c6uue_dz7-66i0ekf2_nj==zs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition
SITE_ID = 1

INSTALLED_APPS = (
    # django apps
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
) + (
    # thirt-party apps
    'django_summernote',
    'rosetta',
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.twitter',
    'sorl.thumbnail',
) + (
    # local apps
    'pyconkr',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'pyconkr.urls'

WSGI_APPLICATION = 'pyconkr.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "pyconkr/templates"),
)


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'pyconkr.db'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

ugettext = lambda s: s
LANGUAGES = (
    ('ko', ugettext('Korean')),
    ('en', ugettext('English')),
    ('ja', ugettext('Japanese')),
)
LANGUAGE_CODE = 'en-us'
MODELTRANSLATION_FALLBACK_LANGUAGES = {
    'default': ('ko', 'en', 'ja'),
}

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "pyconkr/static"),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
STATIC_URL = '/static/'


# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Context processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',

    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',

    'pyconkr.context_processors.default',
    'pyconkr.context_processors.sponsors',
    'pyconkr.context_processors.profile',
)

LOGIN_REDIRECT_URL = '/profile/'
ACCOUNT_EMAIL_REQUIRED = True

DOMAIN = ''

EMAIL_LOGIN_TITLE = ugettext("PyCon Korea 2015 one-time login token")
EMAIL_SENDER = ugettext("PyCon Korea") + "<foo@bar.com>"
EMAIL_USE_TLS = True
EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

CRISPY_TEMPLATE_PACK = 'bootstrap3'

SUMMERNOTE_CONFIG = {
    'toolbar': [
        ['style', ['style']],
        ['style', ['bold', 'italic', 'underline', 'clear']],
        ['para', ['ul', 'ol', 'height']],
        ['insert', ['link']],
        ['misc', ['codeview']],
    ],
    'inplacewidget_external_css': (
    ),
    'inplacewidget_external_js': (
    ),
}

SPEAKER_IMAGE_MAXIMUM_FILESIZE_IN_MB = 5
SPEAKER_IMAGE_MINIMUM_DIMENSION = (500, 500)

IMP_USER_CODE = '---'
IMP_API_KEY = '---'
IMP_API_SECRET = '---'

MAX_TICKET_NUM = 450
TICKET_OPEN_DATETIME = "2015-08-17 12:00:00"
TICKET_CLOSE_DATETIME = "2015-08-24 00:00:00"
