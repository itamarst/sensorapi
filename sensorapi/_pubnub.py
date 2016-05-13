"""
Retrieve records from PubNub and insert into the database.

Potential improvements:

- Better downsampling, e.g. mean of values, time-bases sampling,
  etc. (need to understand implication of sensor_uuid first).
"""
from sys import stdout
from logging import basicConfig, info
from pubnub import Pubnub

from ._db import docker_engine, insert


class Receiver(object):
    """
    Store every Nth PubNub messages in the database.
    """
    def __init__(self, engine, sample):
        """
        sample: sample frequency. 1 means every message, 2 means every
            other, 3 means every third message, etc.
        """
        self._received = 0
        self._sample = sample
        self._engine = engine

    def __call__(self, msg, _):
        if self._received % self._sample == 0:
            msg = msg.copy()  # don't mutate inputs
            for column in [
                    "photosensor", "humidity", "ambient_temperature",
                    "radiation_level", "timestamp"]:
                msg[column] = float(msg[column])
            info("Inserting: {}".format(msg["timestamp"]))
            insert(self._engine, **msg)
        self._received += 1
        return True


def main():
    """
    Run the PubNub client subscription, results of which will get
    inserted into the database (1 out of every 10 messages).
    """
    basicConfig(stream=stdout)
    Pubnub(publish_key='demo',
           subscribe_key='sub-c-5f1b7c8e-fbee-11e3-aa40-02ee2ddab7fe'
    ).subscribe('pubnub-sensor-network',
                callback=Receiver(docker_engine(), 10))
