FROM python:3.11-slim

WORKDIR /app/web/api

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./web/api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./pokedex /app/pokedex
COPY ./challenges /app/challenges
COPY ./web/api/app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
