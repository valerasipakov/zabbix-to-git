# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# (опционально) часовой пояс и сертификаты
RUN apt-get update && apt-get install -y --no-install-recommends tzdata ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# зависимости отдельно — для кеша
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# копируем исходники пакета
COPY tg_bot_dev ./tg_bot_dev

# запускаем как модуль пакета
CMD ["python", "-m", "tg_bot_dev.app"]

