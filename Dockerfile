FROM python:3.7 as backend

RUN apt-get update -qq  \
 && apt-get install -y --no-install-recommends default-mysql-client=1.0.5 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt
WORKDIR /code/

RUN pip install --upgrade pip==20.1.1 \
  && pip install pip-tools==5.2.1 \
  && pip install gunicorn==19.9.0 \
  && pip-sync requirements.txt

COPY . /code/

RUN python manage.py collectstatic --noinput

EXPOSE 8080
CMD exec gunicorn lw.core.wsgi:application --bind 0.0.0.0:8080 --workers 3

FROM nginx:1.18.0-alpine as static
ADD nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=backend /code/lw/static /static
EXPOSE 80
