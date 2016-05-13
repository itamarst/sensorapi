# Sensor REST API

Read data from a pubnub data source, store it in PostgreSQL, expose it via a REST API.


## Architecture

There are multiple of application processes:

1. A reader reads from the PubNub API and writes data into the database.
   If multiple data sources are eventually used multiple processes can be run; initially just one is necessary.
2. A server has a REST API and reads data from the database.
   Since these are read-only stateless processes multiple servers can be run if they become a bottleneck.
3. Database initialization initializes the PostgreSQL schema.


## Packaging

A Docker image includes the base code and allows running the different commands.


## Deployment

Probably Kubernetes on GCE, with:

1. A PostgreSQL container, using a persistent GCE volume for the database.
2. A reader container.
3. A REST API container, publicly exposed over HTTP.
