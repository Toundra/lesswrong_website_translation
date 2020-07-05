APP_NAME=azx9095/lw-django-app
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

build_image:
	docker pull ${APP_NAME}:latest || true
	docker build \
		-t ${APP_NAME}:${VERSION} \
		-t ${APP_NAME}:latest \
		.

push_image:
	docker push ${APP_NAME}:latest
	docker push ${APP_NAME}:${VERSION}
