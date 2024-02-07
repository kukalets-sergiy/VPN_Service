"""
Django settings for vpn_service_core project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from datetime import timedelta
from dotenv import load_dotenv
from pathlib import Path

# Define the path to the .env file, which stores environment variables.
env_path = Path(".") / ".env"
# Load environment variables from the .env file into the current environment.
load_dotenv(dotenv_path=env_path)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

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
    'vpn_service_app',
]


# The unique identifier for the Django site, typically corresponding to a record in the `django_site` database table.
SITE_ID = 1

SITE_URL = 'http://localhost:8000'


# The method used for authentication, in this case, using the email address.
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# Determines the email verification method during user registration. 'none' means no email verification is required.
ACCOUNT_EMAIL_VERIFICATION = 'none'
# Requires users to provide an email address during registration.
ACCOUNT_EMAIL_REQUIRED = True
# Ensures that each email address used for registration is unique across users.
ACCOUNT_UNIQUE_EMAIL = True
# Does not require users to provide a username during registration.
ACCOUNT_USERNAME_REQUIRED = False

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# # Specifies the user model used for user authentication and management in the project.
# # it's set to a custom user model UserData in the "user_management_app."
AUTH_USER_MODEL = "vpn_service_app.UserData"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'vpn_service_core.urls'

# Define the TEMPLATES list, which configures how Django handles templates.
TEMPLATES = [
    {
        # Specify the template backend to use for rendering templates (Django's default backend).
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Define a list of directories to search for templates.
        # In this case, the "templates" directory is in the project's root directory.

        "DIRS": [BASE_DIR / "templates"],
        # "DIRS": ["templates", os.path.join(BASE_DIR, 'docs/_build/html')],
        # Allow Django to look for templates within each installed app.
        "APP_DIRS": True,
        # Configure various template-related options.
        "OPTIONS": {
            # List of context processors that will be applied to the template context.
            # These processors add variables and functionality to the templates.
            "context_processors": [
                # Adds context for debugging (e.g., SQL queries) when DEBUG mode is enabled.
                "django.template.context_processors.debug",
                # Adds the request object to the context, making it available in templates.
                "django.template.context_processors.request",
                # Adds authentication-related context (e.g., logged-in user details) to templates.
                "django.contrib.auth.context_processors.auth",
                # # Adds context for messages framework (e.g., messages used for user feedback).
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = 'vpn_service_core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# # This line specifies the WSGI application for your Django project.
# # WSGI stands for Web Server Gateway Interface, and it is a standard interface
# # between web servers and Python web applications or frameworks.
# WSGI_APPLICATION = "vpn_service_core.wsgi.application"

# Define the database settings for the Django project.
DATABASES = {
    "default": {
        # Set the database engine to PostgreSQL.
        "ENGINE": "django.db.backends.postgresql",
        # Set the name of the database using the POSTGRES_DB environment variable.
        "NAME": os.getenv("POSTGRES_DB"),
        # Set the database user using the POSTGRES_USER environment variable.
        "USER": os.getenv("POSTGRES_USER"),
        # # Set the database password using the POSTGRES_PASSWORD environment variable.
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        # Set the host where the PostgreSQL database is located using the POSTGRES_HOST environment variable.
        "HOST": os.getenv("POSTGRES_HOST"),
        # Set the port to connect to the PostgreSQL database using the POSTGRES_PORT environment variable.
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

VPN_IP_ADDRESSES = os.getenv("VPN_IP_ADDRESSES")

# Define an empty dictionary for the Django Rest Framework settings.
REST_FRAMEWORK = {}

# Configure the settings for the SIMPLE_JWT package for JWT authentication.
# Set the lifetime of access tokens. In this case, access tokens will be valid for 1 day.
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    # Set the lifetime of refresh tokens. In this case, refresh tokens will be valid for 7 days.
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# This setting specifies the URL prefix for static files.
# Static files are files that do not change and can be served directly by a web server.
# In this case, the URL to access static files is "/static/".
STATIC_URL = "/static/"

# STATICFILES_DIRS is a list of directories where Django will look for additional static files.
# It's a list of file system directories, and in this case, it's looking for static
# files within "vpn_service_core/static/".
STATICFILES_DIRS = [os.path.join(BASE_DIR, "vpn_service_core/static/")]


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Set the URL prefix for serving media files.
MEDIA_URL = "/media/"
# Set the absolute filesystem path to the directory where media files will be stored.
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
