.PHONY: build-compose test demo push-image


# Local testing and demonstration:
build-compose:
	docker-compose build

test: build-compose
	docker-compose run api python -m unittest discover

demo: build-compose
	docker-compose up -d
	sleep 10  # Wait for some data to be loaded from PubNub
	curl http://localhost:5000/v1/sensor/humidity | python -mjson.tool
	docker-compose down


# Provision and run on production, i.e. Google Container Engine (Kubernetes)
# Requires PROJECT_NAME environment variable to be set.
push-image:
	test -n "$(PROJECT_NAME)"  # Ensure $$PROJECT_NAME is set
	docker build -t gcr.io/$(PROJECT_NAME)/sensorapi:1.0 .
	gcloud docker push gcr.io/$(PROJECT_NAME)/sensorapi:1.0

provision-cluster:
	gcloud container clusters create --num-nodes=1 test-cluster
	gcloud container clusters get-credentials test-cluster

destroy-cluster:
	gcloud container clusters delete test-cluster

provision-containers:
	kubectl create -f kubernetes/database.yml
	kubectl create -f kubernetes/database-service.yml
	kubectl create -f kubernetes/api.yml
	kubectl create -f kubernetes/subscriber.yml
	kubectl create -f kubernetes/api-service.yml

destroy-containers:
	kubectl delete -f kubernetes/
