FROM python:3.11-slim

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /notifications_api_app

COPY ["poetry.lock", "pyproject.toml", "./"]

RUN pip install "poetry==1.8.4"
RUN poetry install --no-root

COPY notifications_api .

ENTRYPOINT ["python", "main.py"]
