FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app
COPY requirements.txt ./requirements.txt
COPY requirements ./requirements
RUN pip install --no-cache-dir -r requirements.txt -r requirements/dps.txt

COPY app/__init__.py ./app/__init__.py
COPY app/modules/__init__.py ./app/modules/__init__.py
COPY app/modules/DPS ./app/modules/DPS
COPY app/common ./app/common

EXPOSE 8501

CMD ["sh", "-c", "\
    python -m app.modules.DPS & PY_PID=$! ; \
    streamlit run app/modules/DPS/streamlit_app.py \
        --server.headless=true \
        --server.port=8501 & ST_PID=$! ; \
    wait $PY_PID ; EXIT=$? ; kill $ST_PID 2>/dev/null ; exit $EXIT \
"]
