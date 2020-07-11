DJANGO_REGISTRY_NAME=azx9095/lw-django-app
NGINX_REGISTRY_NAME=azx9095/nginx
VERSION = $$(git rev-parse HEAD)

build:
	docker-compose build

dev: build
	docker-compose up

migrate:
	docker-compose exec app ./manage.py migrate

db_setup: migrate
	docker-compose exec app ./manage.py createsuperuser

db_connect:
	docker-compose exec app mysql -h db

dbshell: db_connect

shell:
	docker-compose exec app bash

pyshell:
	docker-compose exec app ./manage.py shell

update_requirements:
	docker cp requirements.in $$(basename `pwd`)_app_1:/code/requirements.in
	docker-compose exec app pip-compile
	docker cp $$(basename `pwd`)_app_1:/code/requirements.txt ./requirements.txt

build_app:
	docker pull ${DJANGO_REGISTRY_NAME}:latest || true
	docker build \
		-t ${DJANGO_REGISTRY_NAME}:${VERSION} \
		-t ${DJANGO_REGISTRY_NAME}:latest \
		.

push_app:
	docker push ${DJANGO_REGISTRY_NAME}:latest
	docker push ${DJANGO_REGISTRY_NAME}:${VERSION}

build_nginx:
	cd infra/nginx && \
	( \
		docker pull ${NGINX_REGISTRY_NAME}:latest || true; \
		docker build \
			-t ${NGINX_REGISTRY_NAME}:${VERSION} \
			-t ${NGINX_REGISTRY_NAME}:latest \
			. \
	)

push_nginx:
	docker push ${NGINX_REGISTRY_NAME}:latest
	docker push ${NGINX_REGISTRY_NAME}:${VERSION}

prepare_container:
	python manage.py collectstatic --noinput
	python manage.py migrate
