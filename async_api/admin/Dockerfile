FROM python:3.10

WORKDIR /opt/app

# Заведите необходимые переменные окружения
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.txt requirements.txt
COPY uwsgi.ini uwsgi.ini
COPY .env .env

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

# Скопируйте всё оставшееся. Для ускорения сборки образа эту команду стоит разместить ближе к концу файла. 
COPY config ./config
COPY movies ./movies
COPY manage.py ./manage.py
COPY static ./static

EXPOSE 8000

ENTRYPOINT ["uwsgi", "--strict", "--ini", "uwsgi.ini"]
# ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
