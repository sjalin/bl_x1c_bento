BCM = 'BCM'
OUT = 'OUT'


def setmode(tmp):
    print(f'Fake GPIO set mode: {tmp}')


def setup(pin, state):
    print(f'Fake GPIO setup: {pin}, {state}')


def output(pin, state):
    print(f'Fake GPIO set pin {pin} to {state}')