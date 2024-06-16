from bluetoothctl import Bluetoothctl
import bluetooth_watchdog as wd
import time
import os
import threading

#TDOD: implement a spawn of "bt-agent --capability=DisplayOnly -p /hme/clem/Projets/gif4000/pins"
# expect("Passkey confirmed")
# expect (UUID)
# if no UUID alors respawn




def init():
    # TODO: check if bt-agent is registered
    agent = Bluetoothctl()
    agent.power("on")
    agent.change_controller_name("gif4000")
    #TODO check if any device present and remove if necessary.
    device = agent.get_available_devices()
    if device:
        print("Oh shit a device")
        address = get_mac_address(device[0])
        agent.remove(address)
    return agent

def start(agent):
    agent.make_discoverable()
    agent.make_pairable()
    agent.device_advertise()

def isClientConnected(agent):
    devices = agent.get_available_devices()
    if not devices:
        return -1
    else:
        return devices[0]

def get_mac_address(client):
    mac_address = client["mac_address"]
    print(mac_address)
    return mac_address

def send_file(path, address):
    command = "timeout 60 bluetooth-sendto --device=" +address + " " + path
    print(command)
    os.system(command)

def clean(agent, client, address):
    if client["mac_address"] == address:
        agent.disconnect(address)
        agent.remove(address)
    else:
        print("client not registered")
def stop(agent):
    agent.power("off")

def watchdog_thread():
    wd.watchdog()

def bt_loop():
    client = -1
    wd_thread = threading.Thread(target=watchdog_thread)
    wd_thread.start()
    bt_controller = init()
    start(bt_controller)
    print("Started")
    try:
        while client == -1:
            print("Connecting ")
            client = isClientConnected(bt_controller)
            print("client", client)
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    address = get_mac_address(client)
    print("got the address")
    time.sleep(20)
    send_file("/home/clem/Projets/gif4000/gif0.gif", address)
    clean(bt_controller, client, address)
    stop(bt_controller)

