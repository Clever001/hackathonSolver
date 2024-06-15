# Проект hackathonSolver

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)

Здесь расположена краткая документация по API проекта.

## Подготовка к работе

### Склонируйте репозиторий себе на локальную машину

Перед установкой скачайте git и python с официальных сайтов, если они не были у вас установлены прежде.

```
git : https://www.git-scm.com/downloads
python: https://www.python.org/downloads/
```

Откройте папку, в которой будет лежать склонированный репозиторий. 
Склонируйте репозиторий.

```
git clone https://github.com/Clever001/hackathonSolver.git
```

Откройте папку hackathonSolver в Pycharm. Введите в терминал следующую команду.

```
.venv\Scripts\activate
```

### Выполните миграции

Перейдите в каталог djangoApi.

```
cd djangoApi
```

Дальше вам требуется создать базу данных. Для этого необходимо провести миграции при помощи следующих команд:

```
python manage.py makemigrations
```

```
python manage.py migrate
```

### Запуск сервера

Запустите сервер при помощи следующей команды. Дождитесь запуска сервера.

```
python manage.py runserver
```

Должны вывестись следующие текстовые данные:

"Django version 5.0.6, using settings 'djangoApi.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK."

### Запуск site.py

Нужно запустить site.py. Для этого откройте еще один терминал, не закрывая старый.
Запустите файл при помощи следующей команды:

```
python site.py
```

На консоль у вас должен вывестись url. Перейдите на него нажав левой кнопкой мыши.
