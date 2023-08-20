FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY webapp .

CMD ["gunicorn", "webapp.wsgi:application", "--bind", "0.0.0.0:8000"]