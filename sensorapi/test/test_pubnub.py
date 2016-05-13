"""
Tests for the pubnub receiver.
"""

from unittest import TestCase

from .common import setup
from .._db import retrieve_sensor
from .._pubnub import Receiver


class ReceiverTests(TestCase):
    """
    Tests for Receiver.
    """
    def setUp(self):
        self.engine = setup(insert_data=False)

    def test_every_nth(self):
        """
        The Receiver inserts every Nth message, in this case 3rd.
        """
        messages = [
            {
                "photosensor": "744.5",
                "humidity": "74.0",
                "sensor_uuid": "probe-1",
                "timestamp": "101",
                "ambient_temperature": "9.25",
                "radiation_level": "{}".format(i + 100.5)
            } for i in range(10)]
        receiver = Receiver(self.engine, 3)
        for m in messages:
            receiver(m)
        self.assertEqual(
            [d["radiation_level"] for d
             in retrieve_sensor(self.engine, "radiation_level")],
            [100.5, 103.5, 106.5, 109.5])

