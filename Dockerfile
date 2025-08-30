FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt  

COPY app ./app
COPY gunicorn_conf.py ./

ENV PORT=8000 HOST=0.0.0.0
EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn_conf.py", "app.main:app" ]
