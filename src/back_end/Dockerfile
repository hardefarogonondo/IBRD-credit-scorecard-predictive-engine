FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./src/back_end /app
COPY ./models /app/models

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]