from setuptools import setup

setup(name='sensorapi',
      version='1.0',
      packages=['sensorapi'],
      entry_points = {
          'console_scripts': ['sensor-subscribe=sensorapi._pubnub:main',
                              'sensor-api=sensorapi._api:main',
          ],
      }
)
