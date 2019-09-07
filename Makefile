dev:
	docker-compose up

migrate:
	docker-compose exec app ./manage.py migrate

db_setup:
	make db_create && python ./manage.py migrate && python ./manage.py createsuperuser

db_create:
	mysql -u root -h db -e 'create database ${DB_NAME}'

db_drop:
	mysql -u root -h db -e 'drop database ${DB_NAME}'

db_connect:
	mysql -h db -u root
