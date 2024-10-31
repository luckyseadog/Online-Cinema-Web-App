FROM python:3.12.3-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow

RUN apt update && apt install \
    gcc \
    libpq-dev \
    libc-dev \
    --no-install-recommends -y && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt .

RUN apt update -y && \
    python -m pip install --upgrade pip && \
    pip3 install -r ./requirements.txt --no-cache-dir

COPY . .

CMD ["/bin/bash", "./entrypoint.sh"]
