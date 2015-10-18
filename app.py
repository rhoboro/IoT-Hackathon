# -*- encoding: utf-8 -*-

import paho.mqtt.client as mqtt
import json
import time

ORG_ID = "u6fmsi"
APP_ID = "98e0d993a8ef"
AUTH_METHOD = "a-u6fmsi-rg0vpw6rer"
AUTH_TOKEN = "3S*rvWkX_&&j1ZTTtO"

DEVICE_TYPE_1 = "business1"
DEVICE_ID_1 = "fcc2de411103"

DEVICE_TYPE_2 = "business2"
DEVICE_ID_2 = "784b87a1a270"

def on_connect(client, userdata, flags, rc):
    client.subscribe("iot-2/type/" + "+"  + "/id/" + "+"  + "/evt/eid/fmt/json", 2)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    print "Get " + str(payload)
    if "light_value" in payload:
        calc_light(payload)
    if "temperature_value" in payload:
        calc_temperature(payload)

def calc_light(payload):
    global device1_light
    global device2_light
    if "device" in payload:
        if payload["device"] == "business1":
            device1_light = payload["light_value"]
        elif payload["device"] == "business2":
            device2_light = payload["light_value"]
            if device1_light - 25 > device2_light:
                dic = {"set_light_value": 1}
            elif device1_light + 25 < device2_light:
                dic = {"set_light_value": 2}
            else:
                dic = {"set_light_value": 0}
            client.publish("iot-2/type/" + DEVICE_TYPE_2  + "/id/" + DEVICE_ID_2 + "/cmd/cid/fmt/json", json.dumps(dic), 2, True)
            print "Sent " + json.dumps(dic) 
    if device1_light < 100:
        send_message("Please turn on the LED.")
    else:
        send_message("")
 
def calc_temperature(payload):
    None
 
def send_message(message):
    dic = {"message": message}
    client.publish("iot-2/type/" + DEVICE_TYPE_1  + "/id/" + DEVICE_ID_1 + "/cmd/cid/fmt/json", json.dumps(dic), 2, True)
    print "Sent " + json.dumps(dic)

device1_light = 770
device2_light = 770
client_id = "a:" + ORG_ID + ":" + APP_ID
endpoint = ORG_ID + ".messaging.internetofthings.ibmcloud.com"
client = mqtt.Client(client_id)
client.username_pw_set(AUTH_METHOD, AUTH_TOKEN)
client.on_connect = on_connect
client.on_message = on_message
client.connect(endpoint, 1883)


while client.loop() == 0:
    None

