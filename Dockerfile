# Autor: Aleksander Szczepocki

FROM python:3.9-slim AS builder
RUN apk add --update curl && \
rm -rf /var/cache/apk/*

FROM python:3.9-slim
WORKDIR /app
COPY server.py requirements /app/
RUN pip install --no-cache-dir -r requirements
EXPOSE 5000

HEALTHCHECK --interval=60s --timeout=10s CMD curl -f http://localhost:5000/ || exit 1

CMD ["python", "server.py"]

