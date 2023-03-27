# Учебный проект: "Блог"
![GitHub Workflow](https://github.com/YaroslavSmrinov/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)
## Описание
Проект для сбора отзывов на всевозможные произведения [искусства](https://ru.wikipedia.org/wiki/%D0%98%D1%81%D0%BA%D1%83%D1%81%D1%81%D1%82%D0%B2%D0%BE), оценки отзывов посредством рейтинга и комментариев к отзывам.

## Технологии
- Python 3.7
- Django 
- Django rest framework
- Docker & Docker-compose
- Nginx
## Запуск проекта в dev-режиме
- Клонируйте репозиторий
```
git clone git@github.com:YaroslavSmrinov/infra_sp2.git
```
### Шаблон наполнения env-файла.
- Создайте и наполните в директории /infra_sp2/infra/ файл .env дефолтными значениями (приведены ниже)
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
### Команды для запуска приложения в контейнерах.
- В директории /infra_sp2/infra соберите образ и запустите контейнеры одной командой
```
docker-compose up -d --build
```
- Выполните миграции
```
docker-compose exec web python manage.py migrate
```
- Создайте пользователя 
```
docker-compose exec web python manage.py createsuperuser
```
- Подгрузите статику
```
docker-compose exec web python manage.py collectstatic --no-input
```
- Для остановки работы и удаления всех контейнеров используйте команду
```
docker-compose down -v
```
### Команды для заполнения базы данными
- Загрузите в контейнер тестовые данные
```
docker cp fixtures.json infra-web-1:/app 
```
- Наполните базу тестовыми данными
```
docker-compose exec web python manage.py loaddata fixtures.json
```
- Для создания бэкапа используйте команду 
```
docker-compose exec web python manage.py dumpdata > <НАЗВАНИЕ ФАЙЛА>.json 
```
однако стоит отметить, что в конец бэкапа нужно будет добавить ']', эта скобка по непонятной причине не добавляется.

### После запуска:
Проект будет доступен по ссылке [http://localhost](http://localhost)
## Автор
- Я
- Смирнов Ярослав
- tg @iaroslav_smirnov