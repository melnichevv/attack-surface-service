FROM python:3.8.3-slim-buster

LABEL maintainer="Vladimir Melnichenko <melnichevv@gmail.com>"

# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    procps \
    vim \
    git \
    && apt-get clean

COPY requirements/ /app/requirements/
COPY scripts/ /app/scripts/

WORKDIR /app

ENV PYTHONPATH /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --requirement /app/requirements/dev.txt

ONBUILD RUN /app/scripts/reset_local_data.sh

CMD python3 manage.py runserver 0.0.0.0:8000
