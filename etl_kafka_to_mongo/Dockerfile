FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim@sha256:444d948934bdb22e3204317842be6e1ad454cfa85103287a2ed18e471ede1f5b

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
