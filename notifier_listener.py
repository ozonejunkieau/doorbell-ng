import paho.mqtt.client as mqtt

from gi.repository import Notify

from notifier_config import MQTT_HOST, MQTT_USERNAME, MQTT_PASSWORD

def on_message(client, userdata, msg):
    if msg.topic == "DOORBELL/RING":
        Notify.Notification.new("The doorbell has been rung!").show()

Notify.init("Doorbell Notifier")

client = mqtt.Client()

client.on_message = on_message
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

client.connect(MQTT_HOST, 1883, 60)
client.subscribe("DOORBELL/RING")

client.loop_forever()
