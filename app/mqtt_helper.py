import os
import ssl
import time
import logging

import paho.mqtt.client as mqtt


class MQTTHelper:

    def __init__(self, sub_callback=None, port=1883):
        """
        :param port: port used by cloud service
        """
        self.connected = False
        self.pending_publishes = []

        # Logging stuff
        logging.basicConfig()
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)

        self.sub_callback = sub_callback

        try:
            self._logger.info("Preparing to initialize")
            self.client_id = f"sub-{time.time()}"
            self.__configure_connection(port)
        except Exception as exc:
            self._logger.info("ERR 500: (__init__ MqttPahoHelper) Failure to instantiate mqtt_helper object: %s", exc)
            return
        else:
            self._logger.info("Connection configured")
        

    def __del__(self):
        self._logger.info("===== CALLING MqttPahoHelper __del__ =====")
        self._client.disconnect() # disconnect gracefully

    def __configure_connection(self, port):
        """
        configures the connection required to successfully communicate with the cloud services
        """

        _self = self
        def on_connect(client, userdata, flags, rc):
            _self.connected = True
            self._logger.debug("===== CLIENT IS CONNECTED calling on_connect =====")
            while len(_self.pending_publishes) > 0:
                msg = _self.pending_publishes.pop()
                self._logger.debug("Publishing message %s %s %s", msg['payload'], " to topic ",  msg['topic'])
                _self._client.publish(msg['topic'], msg['payload'], msg['qos'])

        self._client = mqtt.Client(client_id=self.client_id)
        self._client.on_connect = on_connect
        self._client.on_message = self.sub_callback

        self._logger.info("MqttPahoHelper: start connect")
        endpoint = os.environ.get("MQTT_BROKER_URL")
        self._client.username_pw_set(username="sub_client",password=os.environ.get('SUB_PASSWORD'))

        self._client.connect(endpoint, port=port)

        self._logger.info("MqttPahoHelper: connect success")
        self._client.loop_start()
    
    def subscribe(self, topic):
        self._client.subscribe((topic, 0))

    def publish(self, topic, payload, qos):
        if self.connected:
            # Publish message
            self._logger.info("Publishing message %s to topic %s", payload, topic)
            self._client.publish(topic, payload, qos)
        else:
            # Add message to queue
            self._logger.info("Adding to queue message %s to topic %s", payload, topic)
            self.pending_publishes.append({'topic': topic, 'payload': payload, 'qos': qos})
