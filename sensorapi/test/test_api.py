"""
Tests for the REST API.
"""

from unittest import TestCase
from json import loads

from .common import setup, ENTRIES
from .._api import app


class APITests(TestCase):
    """
    Tests for REST API interaction.
    """
    def setUp(self):
        self.engine = setup()
        self.client = app.test_client()

    def test_retrieve_by_timestamp(self):
        """
        ``/v1/time_range/<start>/<end>`` retrieves full records within the given
        date range.
        """
        # Should retrieve first two records:
        response = self.client.get("/v1/time_range/100/103")
        self.assertEqual(ENTRIES[:2], loads(response.data))

    def test_retrieve_sensor(self):
        """
        ``/v1/sensor/<name>`` returns a particular sensor's values.
        """
        for sensor in ["photosensor", "humidity", "ambient_temperature",
                       "radiation_level"]:
            response = self.client.get("/v1/sensor/" + sensor)
            self.assertEqual(loads(response.data),
                             [{"timestamp": e["timestamp"], sensor: e[sensor]}
                              for e in ENTRIES])
