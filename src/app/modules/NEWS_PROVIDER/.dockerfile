FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app
COPY requirements.txt ./requirements.txt
COPY requirements ./requirements
RUN pip install --no-cache-dir -r requirements.txt -r requirements/news_provider.txt

COPY app/__init__.py ./app/__init__.py
COPY app/modules/__init__.py ./app/modules/__init__.py
COPY app/modules/NEWS_PROVIDER ./app/modules/NEWS_PROVIDER
COPY app/common ./app/common

EXPOSE 8080

CMD ["uvicorn", "app.modules.NEWS_PROVIDER.main:app", "--host", "0.0.0.0", "--port", "8080"]
