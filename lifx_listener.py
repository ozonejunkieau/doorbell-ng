import paho.mqtt.client as mqtt
from lifx.helpers import blink_light

from config import settings

LIFX_LIGHT_MAC = settings.lifx.mac
LIFX_LIGHT_IP = settings.lifx.ip

def on_message(client, userdata, msg):
    if msg.topic == "DOORBELL/RING":
        blink_light(LIFX_LIGHT_MAC, LIFX_LIGHT_IP)

client = mqtt.Client()

client.on_message = on_message
client.username_pw_set(settings.mqtt.username, settings.mqtt.password)

client.connect(settings.mqtt.host, 1883, 60)
client.subscribe("DOORBELL/RING")

client.loop_forever()

