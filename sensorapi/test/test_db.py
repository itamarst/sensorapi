"""
Tests for sensordata._db module.

Potential improvements:

- Use property-based testing to test broader set of inputs and outputs
  (see http://hypothesis.works).
- Be more careful about deleting data so production data is not accidently
  deleted if these tests are run.
"""

from unittest import TestCase

from .common import setup, ENTRIES
from .._db import retrieve_by_timestamp, retrieve_sensor


class DatabaseTests(TestCase):
    """
    Tests for direct database interaction.
    """
    def setUp(self):
        self.engine = setup()

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
        ``retrieve_sensor`` returns a particular column's values.
        """
        for column in ["photosensor", "humidity", "ambient_temperature",
                       "radiation_level"]:
            retrieved = retrieve_sensor(self.engine, column)
            self.assertEqual(map(dict, retrieved),
                             [{"timestamp": e["timestamp"], column: e[column]}
                              for e in ENTRIES])
