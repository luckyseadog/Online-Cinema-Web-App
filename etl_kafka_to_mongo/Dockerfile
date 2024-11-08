FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV PYTHONPATH=/app

WORKDIR /app

RUN apt update -y && apt install \
    git \
    --no-install-recommends -y && apt clean && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .

RUN uv pip install -r requirements.txt --no-cache-dir --system

COPY . .

RUN chmod u+x entrypoint.sh

CMD ["/bin/bash", "./entrypoint.sh"]
