# -*- encoding: utf-8 -*-

import paho.mqtt.client as mqtt
import json
import time
import mraa

LIGHT_UP = 1
LIGHT_DOWN = 2

ORG_ID = "u6fmsi"
TYPE_ID = "business2"
DEVICE_ID = "784b87a1a270"
PASSWORD = "(OGrv4T)S!Nv85QRsc"
THRESHOLD = 400

light = mraa.Aio(0)
led1 = mraa.Gpio(2)
led2 = mraa.Gpio(3)
led3 = mraa.Gpio(4)
led4 = mraa.Gpio(5)
led5 = mraa.Gpio(6)
led6 = mraa.Gpio(7)

led1.dir(mraa.DIR_OUT)
led2.dir(mraa.DIR_OUT)
led3.dir(mraa.DIR_OUT)
led4.dir(mraa.DIR_OUT)
led5.dir(mraa.DIR_OUT)
led6.dir(mraa.DIR_OUT)

leds = [led1, led2, led3, led4, led5, led6]

def on_connect(client, userdata, flags, rc):
    client.subscribe("iot-2/cmd/cid/fmt/json", 2)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    if "set_light_value" in payload:
        set_led_lights(payload["set_light_value"])
    if "set_temperature" in payload:
        set_temperature(payload["set_temperature"])

# LED

def get_current_light_value():
    return light.read()

def get_current_led_value():
    val = 0
    for led in leds:
        val = val + led.read()
    return val

def set_led_lights(cmd):
    print "LED value: " + str(get_current_led_value())
    if cmd == LIGHT_UP:
        print "LIGHT UP"
        val = get_current_led_value() + 1
        for led in leds:
            if val > 0:
                led.write(1)
            else:
                led.write(0)
            val = val - 1
    elif cmd == LIGHT_DOWN:
        print "LIGHT DOWN"
        val = get_current_led_value() - 1
        for led in leds:
            if val > 0:
                led.write(1)
            else:
                led.write(0)
            val = val - 1

# TEMPERATURE
def get_current_temperature_value():
    None

def set_temperature(temperature):
    None

client_id = "d:" + ORG_ID + ":" + TYPE_ID + ":" + DEVICE_ID
endpoint = ORG_ID + ".messaging.internetofthings.ibmcloud.com"
client = mqtt.Client(client_id)
client.username_pw_set("use-token-auth", PASSWORD)
client.on_connect = on_connect
client.on_message = on_message
client.connect(endpoint, 1883)

for led in leds:
    led.write(1)

value = 0
while client.loop() == 0:
    light_value = get_current_light_value()
    msg = json.dumps({"device": "business2", "light_value" :  light_value});
    client.publish("iot-2/evt/eid/fmt/json", msg, 2, True)
    print("sent: " + msg)
    time.sleep(3.0)

