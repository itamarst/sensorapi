# Sensor REST API

Read data from a pubnub data source, store it in PostgreSQL, expose it via a REST API.

## Architecture

There are two different application processes:

1. A reader reads from the PubNub API and writes data into the database.
   If multiple data sources are eventually used multiple processes can be run; initially just one is necessary.
2. A server exposes a REST API and reads data from the database.
   Since these are read-only stateless processes multiple servers can be run if they become a bottleneck.

Each application initializes the database if it's not already initialized.

## Packaging

A Docker image includes the base code and allows running the different commands.

## Local usage

Make sure you have Docker and Docker Compose installed, then run the following:

	$ make demo

This will start 3 Docker processes: PostgreSQL, sensor subscription, and a
REST API on port 5000. It will wait a few seconds to gather data from
PubNub, and then send a query to the REST API. Effectively this is a
end-to-end test.

For tests of internal components, run:

	$ make test

(Be careful not to run the tests against a production database, as
that will delete all data. By default it spins up new Docker images so
that is not a problem.)

## Cloud usage

The software can be deployed to Kubernetes, with included setup for GCE, with:

1. A PostgreSQL container, using a persistent GCE volume for the database.
2. A subscription container.
3. At least one REST API container, publicly exposed over HTTP.

Make sure you have ``gcloud`` installed and initialized for a
particular project with ``gcloud init``, and that you've installed
``kubectl`` via ``gcloud``
(https://cloud.google.com/container-engine/docs/quickstart).

To provision virtual machines and persistent disk:

	$ make provision-cluster
	
To start the containers:

	$ make provision-containers

Once you've started the containers, you can get the external IP of the REST API by running:

	$ kubectl get services

If it's blank, try again in a minute or two.

To shutdown the containers:

	$ make destroy-containers
	
To delete the virtual machines and persistent disk (WARNING: data loss!):

	$ make destroy-cluster

## Potential improvements

* Add password to PostgreSQL for security.
* Separate Docker images for each server, and perhaps separate Python packages etc. if they grow larger.
* Cloud-managed database, rather than running our own.

See the source code for other potential improvements.
