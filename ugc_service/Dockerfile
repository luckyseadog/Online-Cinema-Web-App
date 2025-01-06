FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim@sha256:444d948934bdb22e3204317842be6e1ad454cfa85103287a2ed18e471ede1f5b

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
