FROM python:3.10

ENV PYTHONPATH /opt/app

WORKDIR /opt/app

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--app-dir", "src"]