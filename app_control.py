import asyncio
from ppadb.client import Client as AdbClient


def toggle_screen(phone):
    phone.shell("input keyevent KEYCODE_POWER")

def unlock_phone(phone):
    phone.shell("input touchscreen swipe 930 880 930 380")
    

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

def stop_app(phone):
    phone.shell(
        "am force-stop com.example.accidentgif")


def pull_gif(phone, num):
    gif_name = "/storage/emulated/0/Pictures/gif/res_gif" + str(num) + ".gif"
    file_name = "gif" + str(num) + ".gif"
    phone.pull(gif_name, file_name)
