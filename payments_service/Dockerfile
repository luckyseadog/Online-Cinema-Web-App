FROM python:3.11-slim


ENV PYTHONPATH /app

WORKDIR /app

COPY requirements.txt requirements.txt
COPY entrypoint.sh entrypoint.sh

RUN  pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src/. .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
