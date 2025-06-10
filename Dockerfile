# Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Puedes usar ENTRYPOINT o dejarlo vacío y definir el comando en docker-compose
CMD ["gunicorn", "--config", "gunicorn.conf.py", "backend.wsgi.application"]
