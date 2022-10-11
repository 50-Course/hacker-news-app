#######################
# Dockerfile
# Maintainer: Eri Adeodu (@50-Course)
#######################
FROM python:3.10.4-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt .

# Speed up dependencies, build
#
# See also: https://pythonspeed.com/articles/docker-cache-pip-downloads/
RUN --mount=type=cache,target=/root/.cache pip install -r ./requirements.txt

COPY . /app/
