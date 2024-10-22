FROM python:3.12.3-slim-bookworm

ENV PYTHONPATH /app

RUN apt update && apt install \
    git \
    --no-install-recommends -y && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
