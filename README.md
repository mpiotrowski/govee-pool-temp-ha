# govee-pool-temp-ha
A script to pull Govee pool thermometer (H5109) data into Home Assistant 

# How to run
The sensor needs to be added in configuration.yaml ahead of using the script

To run the script you need to pass a few parameters
- AUTH_TOKEN that you can get from Govee app through a proxy app on your phone
- MQTT_BROKER is broker address/IP
- MQTT_USER/PASSWORD is the auth to MQTT
- SENSOR_NAME is the topic to publish on MQTT

```docker run --restart=always --name govee-pool-thermometer -e AUTH_TOKEN="Bearer ..." -e MQTT_BROKER="homeassistant" -e MQTT_USER=mqtt -e MQTT_PASSWORD=mqtt -e SENSOR_NAME="backyard/pool/temperature" -d mpiotrowski91/govee-pool-thermometer:latest```