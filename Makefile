test:
	docker-compose build
	docker-compose run api python -m unittest discover
