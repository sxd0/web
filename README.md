# QUE
Новые миграции(не нужны)
docker-compose exec app alembic revision --autogenerate -m "init"


docker-compose exec app alembic upgrade head

docker-compose exec db psql -U postgres -d que_db

docker-compose cp seed.sql db:/seed.sql
docker-compose exec db psql -U postgres -d que_db -f /seed.sql

UPDATE users
SET role_id = 1
WHERE id = 4;



## Общая структура
- Все страницы админки доступны по маршруту: /admin
- Используется шаблонизатор Jinja2 и Bootstrap
- Навигация реализована через главную страницу /admin (templates/admin/index.html)

## Технические детали
- Все запросы к данным выполняются через асинхронный SQLAlchemy (async_session_maker)
- Отношения many-to-many реализованы через явную модель QuestionTag, использующую relationship(..., secondary=...)
- Отображение тегов в постах реализовано как viewonly=True связь
- Все шаблоны хранятся в app/admin/templates/admin/
- Все DAO-функции изолированы в admin/*.py, без дублирования логики из API

