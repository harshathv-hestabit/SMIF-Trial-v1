FROM mcr.microsoft.com/azure-functions/python:4-python3.12

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true \
    WEBSITES_INCLUDE_CLOUD_CERTS=true \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/home/site/wwwroot

WORKDIR /home/site/wwwroot

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
COPY requirements ./requirements
RUN pip install --no-cache-dir -r requirements.txt -r requirements/functions.txt


COPY app/__init__.py ./app/__init__.py
COPY app/modules/__init__.py ./app/modules/__init__.py
COPY app/common ./app/common
COPY app/functions/host.json ./host.json
COPY app/functions/change_feed_service ./change_feed_service
COPY app/functions/standard_trigger ./standard_trigger
COPY app/functions/start.sh /home/site/start.sh

RUN chmod +x /home/site/start.sh

CMD ["/home/site/start.sh"]
