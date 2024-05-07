import asyncio
from ppadb.client import Client as AdbClient


def connect_to_phone():
    client = AdbClient(host="127.0.0.1", port=5037)
    print("adb client version", client.version())
    devices = client.devices()
    print("Serial number of connected devices:")
    for device in devices:
        print(device.serial)
    return client.device(devices[0].serial)


def take_photo(phone):
    phone.shell("am broadcast -a com.example.accidentgif.ACTION_SEND\
                            -t text/plain \
                            -e command \"take photo\"\
                            -n com.example.accidentgif/.IntentReceiver")


def erase_dir(phone):
    phone.shell("am broadcast -a com.example.accidentgif.ACTION_SEND\
                            -t text/plain \
                            -e command \"erase\"\
                            -n com.example.accidentgif/.IntentReceiver")


def start_app(phone):
    phone.shell(
        "am start -n com.example.accidentgif/com.example.accidentgif.MainActivity")


def pull_gif(phone, num):
    file_name = "gif" + str(num) + ".gif"
    phone.pull("/storage/emulated/0/Pictures/gif/test.gif", file_name)
