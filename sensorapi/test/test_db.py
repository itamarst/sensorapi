"""
Tests for sensordata._db module.

Potential improvements:

- Use property-based testing to test broader set of inputs and outputs
  (see http://hypothesis.works).
- Be more careful about deleting data so production data is not accidently
  deleted if these tests are run.
"""

from unittest import TestCase

from .._db import (
    docker_engine, insert, retrieve_by_timestamp, retrieve_sensor,
    sensordata)


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


class DatabaseTests(TestCase):
    """
    Tests for direct database interaction.
    """
    def setUp(self):
        self.engine = docker_engine()
        # Cleanup any existing data:
        self.engine.execute(sensordata.delete())
        # Insert test data:
        for entry in ENTRIES:
            insert(self.engine, **entry)

    def test_retrieve_by_timestamp(self):
        """
        ``retrieve_by_timestamp`` retrieves full records within the given
        date range.
        """
        # Should retrieve first two records:
        retrieved = retrieve_by_timestamp(self.engine, 100, 103)
        self.assertEqual(ENTRIES[:2], map(dict, retrieved))

    def test_retrieve_sensor(self):
        """
        ``retrieve_sensor`` returns a particular columns' values.
        """
        for column in ["photosensor", "humidity", "ambient_temperature",
                       "radiation_level"]:
            retrieved = retrieve_sensor(self.engine, column)
            self.assertEqual(map(dict, retrieved),
                             [{"timestamp": e["timestamp"], column: e[column]}
                              for e in ENTRIES])

