"""
Common utilities for testing.
"""

from .._db import docker_engine, insert, sensordata


ENTRIES = [
    {
        "photosensor": 744.5,
        "humidity": 74.0,
        "sensor_uuid": "probe-1",
        "timestamp": 101,
        "ambient_temperature": 9.25,
        "radiation_level": 201
    },
    {
        "photosensor": 745.5,
        "humidity": 75.0,
        "sensor_uuid": "probe-2",
        "timestamp": 102,
        "ambient_temperature": 10.25,
        "radiation_level": 202
    },
    {
        "photosensor": 746.5,
        "humidity": 76.0,
        "sensor_uuid": "probe-3",
        "timestamp": 103,
        "ambient_temperature": 11.25,
        "radiation_level": 203
    }
]

def setup(insert_data=True):
    """
    Clean database, insert entries into the database if requested, and
    return an SQLAlchemy engine.
    """
    engine = docker_engine()
    # Cleanup any existing data:
    engine.execute(sensordata.delete())
    if insert_data:
        # Insert test data:
        for entry in ENTRIES:
            insert(engine, **entry)
    return engine
