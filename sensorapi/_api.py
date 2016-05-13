"""
REST API for retrieving data.

Potential improvements:
- All of the result is serialized into memory; better to write JSON
  directly to response as it is generated.
- Don't do new DB connection per request.
"""

from json import dumps

from flask import Flask, make_response

from ._db import docker_engine, retrieve_by_timestamp, retrieve_sensor


app = Flask(__name__)


def _to_json(entries):
    """
    Convert results from database to JSON response.
    """
    result = [dict(e) for e in entries]
    response = make_response(dumps(result))
    response.headers["content-type"] = "text/json"
    return response


@app.route("/v1/time_range/<int:start>/<int:end>")
def time_range(start, end):
    """
    Return time-range of full entries.
    """
    engine = docker_engine()
    return _to_json(retrieve_by_timestamp(engine, start, end))


@app.route("/v1/sensor/<sensor_name>")
def by_sensor_name(sensor_name):
    """
    Return specific sensor's data.
    """
    engine = docker_engine()
    return _to_json(retrieve_sensor(engine, sensor_name))
