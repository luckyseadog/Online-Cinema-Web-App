# Alembic

* alembic upgrade head - сделать апграйд до последней миграции
* alembic downgrade base - сделать откатить все миграции
* alembic revision -m "Some change in a table" - создать миграцию
* alembic history --verbose - посмотреть историю

# ENVs

В файле **alembic.ini** нужно заменить **sqlalchemy.url**

В файле **postgres_db.py** нужно заменить **dsn**