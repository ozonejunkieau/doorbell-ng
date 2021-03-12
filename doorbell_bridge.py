import requests
import ssl
import asyncio
import zlib
import json
import struct
from time import sleep
from datetime import datetime

import telegram
from loguru import logger
import paho.mqtt.publish as mqttp
from logging_loki import LokiHandler

from config import settings
from unifi.helpers import get_snap_jpeg
from unifi.websocket import get_websocket, decode_update_packet

# Constants from Dynaconf
#######
TELEGRAM_API_KEY = settings.telegram.apikey
TELEGRAM_CHATS = settings.telegram.chat_ids

MQTT_HOST = settings.mqtt.host
MQTT_USERNAME = settings.mqtt.username
MQTT_PASSWORD = settings.mqtt.password

# Configuration of the Unifi
PROTECT_HOST = settings.unifiprotect.host
PROTECT_USER = settings.unifiprotect.username
PROTECT_PASSWORD = settings.unifiprotect.password

# The ID of the doorbell in the unifi system.
DOORBELL_ID = settings.unifidoorbell.device_id
DOORBELL_IP = settings.unifidoorbell.host
DOORBELL_USER = settings.unifidoorbell.username
DOORBELL_PASSWORD = settings.unifidoorbell.password

# Allow ignorance of SSL certificates
VERIFY_SSL = settings.verify_ssl

# Setup logging to Loki if required.
if settings.loki:
    handler = LokiHandler(
        url=settings.loki.host,
        tags={
            "application": "doorbell_bridge",
            },
	version="1"
    )
    logger.add(handler, level="WARNING")


def send_mqtt(msg, data = None):
    mqttp.single(msg, data, hostname=MQTT_HOST, auth={"username": MQTT_USERNAME, "password": MQTT_PASSWORD})

logger.info("Creating Telegram Bot interface.")
bot = telegram.Bot(token=TELEGRAM_API_KEY)

logger.info("Starting Main Websocket Loop")
while True:
    # Retrieve update from websockets stream and recreate if an error occurs.
    try:
        update = ws.recv()
    except NameError:
        # NameError occurs when ws doesn't exist.
        ws = get_websocket(PROTECT_HOST, PROTECT_USER, PROTECT_PASSWORD, VERIFY_SSL)
        continue

    except Exception as e:
        logger.warning(f"Exception (e) whilst receiving from websocket, retrying...")
        sleep(5)
        ws = get_websocket()
        continue

    # Decode this update into the action and payload
    action, payload = decode_update_packet(update)

    # Action the decoded packet
    if action['id'] == DOORBELL_ID or payload.get('camera') == DOORBELL_ID:
        # We care about this update as it relates to the doorbell.
        if action['action'] == 'update':
            # This is a status update, unused at this time. 
            pass

        elif action['action'] == 'add':
            # This is a new event, create a datetime
            event_timestamp = int(payload['start'])
            event_datetime = datetime.fromtimestamp(event_timestamp/1000)
            event_str = event_datetime.strftime('%A %d %B %Y at %H:%M:%S')

            if payload['type'] == 'ring':
                logger.debug(f"Doorbell Ring")

                # The doorbell has been rung, dispatch a MQTT message.
                send_mqtt("DOORBELL/RING", payload['start'])
                
                # Send a Telegram Message to all chats.
                for chat_id in TELEGRAM_CHATS:
                    bot.send_message(chat_id=chat_id, text=f"_\({event_str}\)_\nSomeone at the door for you sir\.\.\.", parse_mode=telegram.ParseMode.MARKDOWN_V2)
                img_bytes = get_snap_jpeg(DOORBELL_IP, DOORBELL_USER, DOORBELL_PASSWORD, VERIFY_SSL)
                for chat_id in TELEGRAM_CHATS:
                    bot.send_photo(chat_id=chat_id, photo=img_bytes)

            elif payload['type'] == 'motion':
                # Motion has been detected, dispatch a MQTT message.
                send_mqtt("DOORBELL/MOTION", payload['start'])
                logger.debug(f"Motion Detected")

            elif payload['type'] == 'smartDetectZone' and 'person' in payload['smartDetectTypes']:
                # A person has been detected, dispatch a MQTT message.
                send_mqtt("DOORBELL/PERSON", payload['start'])
                logger.debug(f"Smart Motion Detected")

            else:
                logger.warning(f"Unknown payload type: {payload['type']}")

        logger.debug(f"ACTION: {action} PAYLOAD: {payload}")




