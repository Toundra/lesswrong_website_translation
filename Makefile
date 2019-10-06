build:
	docker-compose build

dev: build
	docker-compose up

migrate:
	docker-compose run --rm app ./manage.py migrate

db_create:
	docker-compose run --rm app mysql -u root -h db -e 'CREATE DATABASE IF NOT EXISTS lw'

db_setup: db_create
	docker-compose run --rm app bash -c 'python ./manage.py migrate && python ./manage.py createsuperuser'

db_drop:
	docker-compose run --rm app mysql -u root -h db -e 'DROP DATABASE lw'

db_connect:
	docker-compose run --rm app mysql -h db -u root
