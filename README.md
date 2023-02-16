# diplom10
# Дипломный проект PD10 на Django

# Cтек (python3.9, Django, Postgres)

# Запуск проекта:
---1---
# Для установки зависимостей используем Poetry:
pip install poetry
- для первичной установки
poetry install
- для обновления
poetry update

---2---
# Задание переменных окружения при помощи .env:
SECRET_KEY=django-insecure-$y)+22f2&kto59l3pgs#x&*5zen%-v5j=132445k*wwwd5t
DEBUG=True
POSTGRES_USER=sasha
POSTGRES_DB=diplom
POSTGRES_PASSWORD=123456

---3---
# Создание контейнера в Docker (docker-compose.yaml) с Postgres:
docker-compose up -d

---4---
# Создание и применение миграций:
python manage.py makemigrations
python manage.py migrate

---5---
# Запуск проекта
python manage.py runserver
