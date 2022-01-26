import os
import json

import time
import logging

from PIL import Image
from paho.mqtt.client import MQTTMessage, Client

from app.message_processor import MessageProcessor
from app.mqtt_helper import MQTTHelper
from app.slideshow import Slideshow

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

slideshow=Slideshow('/dev/fb0')


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
        fname=f'./photos/{time.time()*10:.0f}.png'
        img.save(fname})
        slideshow.add_image(fname)

    else:
        logger.warning('not valid fields in message: %s', message)


mqtt = MQTTHelper(sub_callback=sub_callback)
mqtt.subscribe(os.environ.get('TOPIC'))
slideshow.start_slideshow()
