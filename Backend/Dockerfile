FROM python:3.9-slim AS base

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM base AS runtime
COPY . .

CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000"]
