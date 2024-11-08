FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow

WORKDIR /app

RUN apt update -y

COPY ./requirements.txt .

RUN uv pip install -r requirements.txt --no-cache-dir --system

COPY . .

EXPOSE 8000

RUN chmod u+x entrypoint.sh

CMD ["/bin/bash", "./entrypoint.sh"]
