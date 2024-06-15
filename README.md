# Проект hackathonSolver

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)

Здесь расположена краткая документация по API проекта.

## Подготовка к работе

### Склонируйте репозиторий себе на локальную машину

```
git clone https://github.com/Clever001/hackathonSolver.git
```

### Установите требуемые пакеты

Для работы проекта требуется установить некоторые пакеты.

```
pip install -r requirements.txt
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

### Проинициализируйте БД

Перед работой требуется проицициализировать в базе данных некоторые данные.
Для этого перейдите в папку beforeRun и запустите файл Init DataBase.py

### Запуск сервера

Зайдите в консоль и перейдите в каталог djangoApi.
Запустите сервер при помощи следующей команды.

```
python manage.py runserver
```

## Документация

Api было полностью перевормулировано с целью ускорения работы и упрощения реализации фронтенда. 
Теперь не требуется авторизация пользователя. Запросы разрешается отправлять любому пользователю.

### Запрос AskQuestion

Данный запрос сразу проводит токенизацию. После сохраняет результат в бд. Потом проводит классификацию. 
Тоже сохраняет результат в бд. И уже после запускает трансформер для более выбора наиболее релевантного ответа.

```
url: http://127.0.0.1:8000/api/v1/ask_question/
Methods: GET.
```

Пример входных данных:

```json
{
    "message": "Как можно отдохнуть?"
}
```

Пример выходных данных: (status: 200 OK)

```json
{
    "answer": "Watch youtube."
}
```

В случае если запрос был пустой, выводит ошибку: (status: 400 BAD REQUEST)

```json
{
    "error": "Message cannot be empty."
}
```

### Запрос Docs

Данный запрос служит для инициализации базы данных. 
Разрешается работать с конкретной записью в бд при помощи индекса pk, но это не обязательно.

```
url: http://127.0.0.1:8000/api/v1/docs/
Methods: GET, POST, DELETE.
```

Вход: (POST)

```json
{
    "file": "Какое-то название.pdf",
    "title": "Какой-то заголовок",
    "answer": "Какой-то ответ"
}
```

Выход: (status: 201 Created)

```json
{
    "file": "Какое-то название.pdf",
    "title": "Какой-то заголовок",
    "answer": "Какой-то ответ"
}
```
