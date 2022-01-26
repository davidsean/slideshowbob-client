import os
import json
import time
import logging

from PIL import Image
from app.message_processor import MessageProcessor
from app.mqtt_helper import MQTTHelper
from paho.mqtt.client import MQTTMessage, Client

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def sub_callback(client:Client, userdata, message:MQTTMessage) -> None:
    """
    """
    print(message.payload)
    try:
        payload: dict = json.loads(message.payload)
    except (json.JSONDecodeError, TypeError) as exc:
        logger.error(exc)
        return
    logger.info("Received from subscriber: %s", payload)
    if 'url' in payload and 'sender_id' in payload:
        image_url = payload['url']
        sender_id = payload['sender_id']
        mp = MessageProcessor(image_url, sender_id)
        img:Image.Image = mp.process_post()
        img.save('bleh.png')
    else:
        logger.warning('not valid fields in message: %s', message)


if __name__ == '__main__':
    mqtt = MQTTHelper(sub_callback=sub_callback)
    mqtt.subscribe(os.environ.get('TOPIC'))
    while True:
        time.sleep(1)