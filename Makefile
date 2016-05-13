.PHONY: build test demo

build:
	docker-compose build

test: build
	docker-compose run api python -m unittest discover

demo: build
	docker-compose up -d
	sleep 10  # Wait for some data to be loaded from PubNub
	curl http://localhost:5000/v1/sensor/humidity | python -mjson.tool
	docker-compose down
