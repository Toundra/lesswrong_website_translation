FROM python:3.7

RUN apt-get update -qq  \
 && apt-get install -y --no-install-recommends default-mysql-client=1.0.5 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt
WORKDIR /code/

RUN pip install --upgrade pip==20.1.1 \
  && pip install pip-tools==5.2.1 \
  && pip-sync \
  && pip install gunicorn==19.9.0

COPY . /code/

EXPOSE 80
CMD exec gunicorn lw.core.wsgi:application --bind 0.0.0.0:80 --workers 3
