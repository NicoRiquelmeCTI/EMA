# python 3.6

import random
import time
import json
from paho.mqtt import client as mqtt_client
from random import randrange, uniform

broker = 'ema.con-ciencia.cl'
port = 1883
topic = "v1/devices/me/telemetry"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = "qgfFBxXrhjm1jBBinfb0"
password = None
payload = {"altitud_bme":0, "decibeles":123, "humedad_pms":8, "pm01":18, "pm10":26, "pm25":33, "presion_bme": 19, "temperatura_bme":24, "temperatura_pms":241, "viento":21}
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(3)
        msgc = f"messages: {msg_count}"
        payload = {
            "altitud_bme":123,
            "decibeles":randrange(80, 120),
            "humedad_pms":randrange(9, 20),
            "pm01":randrange(15, 51),
            "pm10":randrange(15,60),
            "pm25":randrange(6,30),
            "presion_bme": uniform(1.001, 1.21),
            "temperatura_bme":uniform(20.3, 28.4),
            "temperatura_pms":uniform(20.3, 28.4),
            "viento":uniform(0.006, 12.63)
            }

        result = client.publish(topic, json.dumps(payload))
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msgc}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
