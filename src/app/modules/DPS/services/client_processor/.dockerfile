FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/__init__.py ./app/__init__.py
COPY app/modules/__init__.py ./app/modules/__init__.py
COPY app/modules/DPS ./app/modules/DPS
COPY app/common ./app/common

CMD ["python", "-m", "app.modules.DPS.services.client_processor"]
