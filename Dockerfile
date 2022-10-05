#######################
# Dockerfile
# Maintainer: Eri Adeodu (@50-Course)
#######################
FROM python:3.10.4-slim-bullseye as builder

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r ./requirements.txt

COPY . /app/