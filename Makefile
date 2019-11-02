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
