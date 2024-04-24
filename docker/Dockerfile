FROM python:3
LABEL authors="dkhorkov, hikfee"

WORKDIR /app

COPY . /app

# Changing permissions for correct work inside docker:
RUN chmod +x /app/docker/entrypoint.sh

RUN pip install -r requirements/prod.txt
