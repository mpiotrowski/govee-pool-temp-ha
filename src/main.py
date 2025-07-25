import logging
import time
import os
import sys

import paho.mqtt.publish as publish
import requests
import json

import threading
import schedule

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("Govee Pool Thermometer")

auth_token = os.environ['AUTH_TOKEN']
mqtt_broker = os.environ['MQTT_BROKER']
mqtt_user = os.environ['MQTT_USER']
mqtt_password = os.environ['MQTT_PASSWORD']
mqtt_sensor = os.environ['SENSOR_NAME']

if auth_token is None or mqtt_broker is None or mqtt_sensor is None:
    logger.error("One of the settings wasn't provided, finishing")
    sys.exit(1)

def check_temp_and_publish():
    # Make an HTTP GET request
    response = requests.get(
            url="https://app2.govee.com/bff-app/v1/device/list",
            headers={
                "Host": "app2.govee.com",
                "Authorization": auth_token,
                "Accept": "*/*",
                "envId": "0",
                "clientId": "5a94738ed5c84265a6f40045a1119383",
                "appVersion": "7.0.12",
                "Accept-Language": "en",
                "sysVersion": "18.5",
                "clientType": "1",
                "User-Agent": "GoveeHome/7.0.12 (com.ihoment.GoVeeSensor; build:3; iOS 18.5.0) Alamofire/5.6.4",
                "Connection": "keep-alive",
                "timezone": "America/New_York",
                "country": "US",
                "iotVersion": "0",
                "Content-Type": "application/json",
            }
        )

    if response.status_code == 200:
        for device in response.json()['data']['devices']:
            if device['sku'] == "H5109":
                data = json.loads(device['deviceExt']['lastDeviceData'])
                temperature = data['tem'] / 100.0
                logger.info(f"Temperature: {temperature}°C")
                temperature_f = (temperature * 9/5) + 32
                logger.info(f"Temperature: {temperature_f}°F")
                publish.single(
                    mqtt_sensor,
                    payload=temperature_f,
                    qos=1,
                    retain=True,
                    hostname=mqtt_broker,
                    port=1883,
                    auth={'username': mqtt_user, 'password': mqtt_password}
        )
    else:
        logger.error("Failed to retrieve data:", response.status_code)

def run_thread(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every(5).minutes.do(run_thread, check_temp_and_publish).run()

if __name__ == "__main__":

    while True:
        schedule.run_pending()
        time.sleep(1)