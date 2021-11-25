# print("hello")

# разрешаем выполнение локальных скриптов - нобходимо для запуска virtualenv
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# ../pomm/Scripts/activate - запускаем virtualenv

# pip install django
# pip install psycopg2
# pip install social-auth-app-django
# django-admin startproject books_api

# в VSCode выбираем ./books_app как папку проекта
# ./manage.py startapp store

# создаем бд и прописываем в settings.py
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'books_db',
#         'USER': 'books_user',
#         'PASSWORD': '12345',
#     }
# }
# python manage.py migrate
# python manage.py createsuperuser
# python manage.py runserver

# создать модель
# python manage.py makemigrations
# python manage.py migrate 

# http://127.0.0.1:8000/book/?format=json

# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "books.settings")
# django.setup()

# python manage.py test store.tests .
# python manage.py test store.tests.test_api.BooksApiTestCase.test_create

# GitHub Auth
# bezCianApp
# https://github.com/settings/applications/1767897
# SOCIAL_AUTH_POSTGRES_JSONFIELD = True
# SOCIAL_AUTH_GITHUB_KEY = '62b5d48f460bfa9f6f3a'
# SOCIAL_AUTH_GITHUB_SECRET = 'adc3c60bbd0f11988d7ea722c39df34da7b18e9e'

# >>> user = User.objects.get(id=1)
# >>> user.books.all()
# >>> user.my_books.all()











# Package                Version
# ---------------------- ---------
# asgiref                3.4.1
# autopep8               1.6.0
# certifi                2021.10.8
# cffi                   1.15.0
# charset-normalizer     2.0.7
# cryptography           35.0.0
# defusedxml             0.7.1
# Django                 3.2.9
# django-filter          21.1
# django-rest-framework  0.1.0
# djangorestframework    3.12.4
# idna                   3.3
# oauthlib               3.1.1
# pip                    21.3.1
# psycopg2               2.9.2
# pycodestyle            2.8.0
# pycparser              2.21
# PyJWT                  2.3.0
# python3-openid         3.2.0
# pytz                   2021.3
# requests               2.26.0
# requests-oauthlib      1.3.0
# setuptools             58.3.0
# social-auth-app-django 5.0.0
# social-auth-core       4.1.0
# sqlparse               0.4.2
# toml                   0.10.2
# urllib3                1.26.7
# wheel                  0.37.0

# echo "# bezcian-api" >> README.md
# git init
# git add README.md
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/levtrilev/bezcian-api.git
# git push -u origin main
#
#
# …or push an existing repository from the command line
# git remote add origin https://github.com/levtrilev/bezcian-api.git
# git branch -M main
# git push -u origin main