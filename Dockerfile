FROM python:3.12-slim

WORKDIR /app

# Tezroq build uchun layer
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Loyiha
COPY bot ./bot
COPY data ./data

# Persisted DB papkasi
RUN mkdir -p /app/data

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Demo xonadonlarni seed qilish + botni ishga tushirish
CMD ["sh", "-c", "python -m bot.seed && python -m bot.main"]
