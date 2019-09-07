dev:
	docker-compose up

migrate:
	docker-compose exec app ./manage.py migrate

shell:
	docker-compose exec app bash

dbshell:
	docker-compose exec db mysql lw

pyshell:
	docker-compose exec db ./manage.py shell
