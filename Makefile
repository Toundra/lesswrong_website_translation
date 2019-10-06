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
