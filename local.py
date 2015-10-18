# -*- encoding: utf-8 -*-

import paho.mqtt.client as mqtt
import json
import time
import mraa

ORG_ID = "u6fmsi"
TYPE_ID = "business1"
DEVICE_ID = "fcc2de411103"
PASSWORD = "5o7vo(ogXvOd6Hijww"


def on_connect(client, userdata, flags, rc):
    client.subscribe("iot-2/cmd/cid/fmt/json")

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    if "message" in payload:
        print payload
        set_message(payload["message"])

def get_current_light_value():
    return mraa.Aio(0).read() 

def get_current_temperature_value():
    None

def set_message(msg):
    # msgを表示する
    None

endpoint = ORG_ID + ".messaging.internetofthings.ibmcloud.com"
client = mqtt.Client(client_id)
client.username_pw_set("use-token-auth", PASSWORD)
client.connect(endpoint, 1883)

while client.loop() == 0:
    light_value = get_current_light_value()
    msg = json.dumps({"device": "business1", "light_value" :  light_value});
    client.publish("iot-2/evt/eid/fmt/json", msg, 0, True)
    print("sent: " + msg)
    time.sleep(1.5)

