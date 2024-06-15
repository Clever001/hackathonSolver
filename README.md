# Проект hackathonSolver

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)

Здесь расположена краткая документация по API проекта.

## Подготовка к работе

### Склонируйте репозиторий себе на локальную машину

Склонируйте репозиторий и создайте виртуальное окружение .venv.

### Установите требуемые пакеты

Для работы проекта требуется установить некоторые пакеты.

```
pip install django, djangorestframework, djangorestframework-simplejwt
pip install numpy, pandas, requests, pywebio, torch, transformers
pip install scikit-learn, sentence-transformers, torchvision
pip install torchaudio, asyncio, pywebio, openpyxl
```

### Сделайте миграции

Откройте терминал, перейдите в каталог проекта. После перейдите в каталог djangoApi

```
cd djangoApi
```

Дальше вам требуется создать свою базу данных. Для этого необходимо провести миграции при помощи следующих команд:

```
python manage.py makemigrations
```

```
python manage.py migrate
```

### Запуск сервера

Зайдите в консоль и перейдите в каталог djangoApi.
Запустите сервер при помощи следующей команды.

```
python manage.py runserver
```

### Проинициализируйте БД

Перед работой требуется проицициализировать в базе данных некоторые данные.
Для этого перейдите в папку beforeRun и запустите файл Init DataBase.py
