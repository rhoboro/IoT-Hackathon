# -*- encoding: utf-8 -*-

import paho.mqtt.client as mqtt
import pyupm_i2clcd as lcd

import json
import time
import mraa

ORG_ID = "u6fmsi"
TYPE_ID = "business1"
DEVICE_ID = "fcc2de411103"
PASSWORD = "5o7vo(ogXvOd6Hijww"

lcd_display = lcd.Jhd1313m1(6, 0x3E, 0x62)

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
    if msg == "":
        lcd_display.clear()
        lcd_display.setColor(0, 0, 0)
    else:
        lcd_display.setCursor(0, 0)
        lcd_display.setColor(255, 0, 0)
        lcd_display.write(str(msg))
        lcd_display.scroll(True)

client_id = "d:" + ORG_ID + ":" + TYPE_ID + ":" + DEVICE_ID
endpoint = ORG_ID + ".messaging.internetofthings.ibmcloud.com"
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("use-token-auth", PASSWORD)
client.connect(endpoint, 1883)

while client.loop() == 0:
    light_value = get_current_light_value()
    msg = json.dumps({"device": "business1", "light_value" :  light_value});
    client.publish("iot-2/evt/eid/fmt/json", msg, 0, True)
    print("sent: " + msg)
    time.sleep(1.5)

