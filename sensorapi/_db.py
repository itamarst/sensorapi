"""
Database schema and API for storing sensor data.

Potential improvements:
- All data is loaded into memory; better to provide streaming API.
- Retrying database connection forever is a problem; need timeouts,
  logging, differentiation between different kinds of errors, etc..
"""

from time import sleep

from sqlalchemy import (
    MetaData, Table, Column, String, Float, create_engine, select,
    and_)
from sqlalchemy.exc import OperationalError

metadata = MetaData()

# Schema for the records. We add index on timestamp since we need to
# support time-based range queries.
sensordata = Table("sensordata", metadata,
                   Column("timestamp", Float, index=True),
                   Column("sensor_uuid", String(30)),
                   Column("humidity", Float),
                   Column("photosensor", Float),
                   Column("radiation_level", Float),
                   Column("ambient_temperature", Float))


__all__ = ["docker_engine", "insert", "retrieve_by_timestamp",
           "retrieve_sensor"]


def docker_engine():
    """
    Create a SQLAlchemy Engine pointed at a PostgreSQL server run by Docker.

    Specifically, the assumption is that the hostname is
    "sensordb", and username/password/dbname are "postgres".

    Tables will be created if necessary.
    """
    engine = create_engine(
        "postgresql+psycopg2://{}:{}@{}/{}".format(
            "postgres", "postgres", "sensordb", "postgres"))
    # Database may be starting up or temporarily unavailable, so retry:
    while True:
        try:
            metadata.create_all(engine)
        except OperationalError:
            sleep(0.1)
        else:
            break
    return engine


def insert(engine, **params):
    """
    Insert a new record.
    """
    insert = sensordata.insert().values(**params)
    engine.execute(insert)


def retrieve_by_timestamp(engine, start, end):
    """
    Return full records for timestamps (seconds since epoch UTC)
    between start and end.
    """
    query = select([sensordata]).where(
        and_(sensordata.c.timestamp >= start,
             sensordata.c.timestamp < end)).order_by(sensordata.c.timestamp)
    return engine.execute(query).fetchall()


def retrieve_sensor(engine, sensor_name):
    """
    Retrieve all values for a particular sensor.
    """
    if sensor_name not in ("humidity", "ambient_temperature", "radiation_level",
                           "photosensor"):
        raise RuntimeError("Unknown sensor name.")
    query = select([getattr(sensordata.c, sensor_name), sensordata.c.timestamp])
    query = query.order_by(sensordata.c.timestamp)
    return engine.execute(query).fetchall()
