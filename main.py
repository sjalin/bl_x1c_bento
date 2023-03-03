import json

import paho.mqtt.client as mqtt
import time
import ssl
import certifi

try:
    import config
except Exception as e:
    print(f"NO VALID CONFIG FILE (./config.py) {e}")
    exit()

connected = None


def on_connect(client, userdata, flags, rc):
    global connected
    if rc == 0:
        print(f'[I] Connected to printer {client} {userdata} {flags}')
        connected = True
    else:
        print('[E] Connection failed')
        connected = False


def handle_message(payload):
    print(json.loads(payload))


def on_message(client, userdata, message):
    if message.topic != f'device/{config.printer_sn}/report':
        print(f'[E] Unknown topic {message.topic}, msg = {str(message.payload.decode("utf-8"))}')
    else:
        handle_message(message.payload)


def connect(mqtt_client):
    mqtt_client.username_pw_set(username=config.printer_username, password=config.printer_password)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.tls_set(certifi.where(), cert_reqs=ssl.CERT_NONE)

    mqtt_client.connect(config.printer_ip, port=config.printer_port)
    mqtt_client.loop_start()

    attempts = 0

    while connected is None and attempts < 10:
        print(connected)
        print('[I] Connecting...')
        time.sleep(1)
        attempts += 1

    if not connected:
        print("[E] Could not connect to printer")
        return False

    print('[I] Connection complete')


def main():
    mqtt_client = mqtt.Client()

    connect(mqtt_client)

    mqtt_client.loop_start()
    mqtt_client.subscribe(f'#')

    while True:
        time.sleep(10)
        print('.')


if __name__ == '__main__':
    main()