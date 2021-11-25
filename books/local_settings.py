from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-vdw1n#ia_=&y4$6m=20pdyr-o^!@3)2!s3mii!mba2bz7at-_v'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'books_db',
        'USER': 'books_user',
        'PASSWORD': '12345',
    }
}

STATIC_URL = '/static/'