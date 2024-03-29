import datetime
import json
from enum import Enum

import paho.mqtt.client as mqtt
import time
import ssl
import certifi

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    import fake_gpio as GPIO


try:
    import config
except Exception as e:
    print(f'[E] NO VALID CONFIG FILE (./config.py) {e}')
    exit()

FAN_PIN = 17
LED_PIN = 13


connected = None
turn_off_time = time.time()
last_gcode_status = 'NONE'


class GCodeStates(Enum):
    IDLE = 'IDLE'
    RUNNING = 'RUNNING'
    FAILED = 'FAILED'
    FINISH = 'FINISH'


def on_connect(client, userdata, flags, rc):
    global connected
    if rc == 0:
        print(f'[I] Connected to printer {client} {userdata} {flags}')
        connected = True
    else:
        print('[W] Connection failed')
        connected = False


def handle_message(payload):
    global turn_off_time
    global last_gcode_status

    json_payload = json.loads(payload)
    # print(f'[D] {json_payload}')
    if 'print' in json_payload.keys():
        try:
            gcode_state = json_payload['print']['gcode_state']
            if gcode_state != last_gcode_status:
                print(f'[I] STATUS: {last_gcode_status} -> {gcode_state}')
                last_gcode_status = gcode_state
                if gcode_state != GCodeStates.RUNNING.value:
                    if time.time() >= turn_off_time:
                        print(f'[I] Fan off')
                        GPIO.output(FAN_PIN, False)
                        GPIO.output(LED_PIN, False)
                    else:
                        print(f'[I] fan pending off in {turn_off_time - time.time()} s')
                else:
                    print(f'[I] Fan on')
                    turn_off_time = time.time() + 120
                    GPIO.output(FAN_PIN, True)
                    GPIO.output(LED_PIN, True)
        except KeyError as e:
            print(f'[W] got KeyError {e}. payload: {json_payload}')


def on_message(client, userdata, message):
    if message.topic != f'device/{config.printer_sn}/report':
        print(f'[W] Unknown topic {message.topic}, msg = {str(message.payload.decode("utf-8"))}')
    else:
        handle_message(message.payload)


def connect(mqtt_client):
    mqtt_client.username_pw_set(username=config.printer_username, password=config.printer_password)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.tls_set(certifi.where(), cert_reqs=ssl.CERT_NONE)

    while True:
        try:
            mqtt_client.connect(config.printer_ip, port=config.printer_port)
            break
        except OSError as e:
            print(f'[W] No network yet: {e}')
            time.sleep(5)

    mqtt_client.loop_start()

    while connected is None:
        print('[I] Connecting...')
        time.sleep(5)

    if not connected:
        print('[W] Could not connect to printer')
        return False

    print('[I] Connection complete')


def gpio_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT)
    GPIO.output(FAN_PIN, False)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, False)


def main():
    gpio_setup()
    mqtt_client = mqtt.Client()
    connect(mqtt_client)
    mqtt_client.loop_start()
    mqtt_client.subscribe(f'#')

    while True:
        time.sleep(300)
        print(f'[I] {datetime.datetime} still alive')


if __name__ == '__main__':
    main()