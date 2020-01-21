"""
Django settings for panopticum project.

Generated by 'django-admin startproject' using Django 2.1.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pq9o2n(8u4j57yium2v9xoqnzqnri9j2#+_wy3*%eo^bvowq1w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_datatables',
    'django_extensions',
    'django_filters',
    'corsheaders',
    'admin_reorder',
    'simple_history',
    'panopticum'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_datatables.renderers.DatatablesRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework_datatables.filters.DatatablesFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_datatables.pagination.DatatablesPageNumberPagination',
    'PAGE_SIZE': 50,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
    'simple_history.middleware.HistoryRequestMiddleware'
]

ROOT_URLCONF = 'panopticum_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'panopticum.context_processors.page_content'
            ],
        },
    },
]

WSGI_APPLICATION = 'panopticum_django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# JIRA

JIRA_CONFIG = { }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Admin panel view
# https://github.com/mishbahr/django-modeladmin-reorder

ADMIN_REORDER = (
    # Keep original label and models
    'sites',

    {'app': 'auth', 'models': ('panopticum.User', 'auth.Group')},

    {'app': 'panopticum', 'label': 'Components', 'models':
        ('panopticum.ComponentVersionModel',)
    },

    {'app': 'panopticum', 'label': 'Products', 'models':
        ('panopticum.ProductFamilyModel', 'panopticum.ProductVersionModel')
    },

    {'app': 'panopticum', 'label': 'Deployments', 'models':
        ('panopticum.DeploymentLocationClassModel', 'panopticum.DeploymentEnvironmentModel', 'panopticum.TCPPortModel')
    },

    {'app': 'panopticum', 'label': 'Active Directory', 'models':
        ('panopticum.CountryModel', 'panopticum.OrganizationModel', 'panopticum.OrgDepartmentModel',
         'panopticum.PersonRoleModel', 'panopticum.PersonModel')
    }
)


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Page content

PAGE_TITLE = "Components Registry"
PAGE_FOOTER = "Copyright © 2019"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


AUTH_USER_MODEL = 'panopticum.User'


curr_dir = os.path.abspath(os.path.dirname(__file__))
if os.path.exists(os.path.join(curr_dir, "settings_local.py")):
    sys.path.append(curr_dir)
    from settings_local import *
