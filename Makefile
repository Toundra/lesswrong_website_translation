dev:
	docker-compose up

migrate:
	docker-compose exec app ./manage.py migrate
