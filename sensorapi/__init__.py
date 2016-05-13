"""
Read data from PubNub, write to Postgres, expose via REST API.

Sample data from PubNub:

{
    photosensor: 744.06,
    humidity: 74.9029,
    sensor_uuid: probe-62568597,
    timestamp: 1450259348,
    ambient_temperature: 9.669,
    radiation_level: 201
}

"""
