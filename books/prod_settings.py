from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-vdw1n#ia_=&y4$6m=20-o^!857jt8j5y48758dw9r8d47*&J*&*(#(*7at-_v'

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bezcian',
        'USER': 'bcadmin',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_URL = '/static/'