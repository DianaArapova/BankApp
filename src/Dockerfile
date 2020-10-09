# pull official base image
FROM python:3.8.3-alpine

# set work directory
ENV APP_HOME=$APP_HOME
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt $APP_HOME

# install dependencies
RUN set -eux
RUN apk add --no-cache --virtual .build-deps build-base \
    libressl-dev libffi-dev gcc musl-dev postgresql-dev python3-dev
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /usr/src/app/requirements.txt
RUN rm -rf /root/.cache/pip

# copy entrypoint.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

# RUN black /usr/src/app/app
# RUN isort /usr/src/app/app

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
