FROM mcr.microsoft.com/azure-functions/python:4-python3.12

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/home/site/wwwroot

WORKDIR /home/site/wwwroot

RUN pip install --no-cache-dir \
    azure-functions==1.24.0 \
    azure-servicebus==7.14.2

COPY app/__init__.py ./app/__init__.py
COPY app/modules/__init__.py ./app/modules/__init__.py
COPY app/common ./app/common
COPY app/modules/EH_DISPATCHER ./EH_DISPATCHER
