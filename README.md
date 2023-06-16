# To-do-list
![To-do-list workflow](https://gitlab.com/Edw125/notification-service/badges/main/pipeline.svg)
## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitLab](https://img.shields.io/badge/-GitLab-464646?style=flat-square&logo=GitLab)](https://gitlab.mplab.io/)
## Описание проекта
* Тестовый API сервис
## Документация к API
* Документация к API можно посмотреть тут: 
[http://127.0.0.1:8000/api/v1/schema/swagger-ui/](http://127.0.0.1:8000/api/v1/schema/swagger-ui/)
[http://127.0.0.1:8000/api/v1/schema/redoc/](http://127.0.0.1:8000/api/v1/schema/redoc/)
## Запуск проекта в Docker контейнере
* Склонировать репозиторий и перейти в него в командной строке:
```bash
git clone git@github.com:Edw125/To-do-list.git
cd To-do-list
```
* Установите Docker
* Отредактируйте или создайте файл `.env` в root. Добавьте в него `TELEGRAM_TOKEN`
* Параметры запуска описаны в файлах `docker-compose.yml` которые находятся в корне.
* Запустите docker compose:
```bash
docker compose up -d --build
```
* Создайте миграции:
```bash
docker compose exec server python manage.py makemigrations
```
* Примените миграции:
```bash
docker compose exec server python manage.py migrate
```
* Перед тем, как войти в админ-панель, нужно создать суперпользователя командой:
```bash
docker compose exec server python manage.py createsuperuser
```
## Доступ к админ-зоне
* Доступ к админ-зоне можно получить тут:
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
