from bluetoothctl import Bluetoothctl


import os
import pexpect
import sys
import subprocess
import logging
import time


# Not a real WD since no kick does not trigger anything. This module is intended
# to handle disconnections and faulty pairing

def start_bt_agent():
    agent = pexpect.spawnu("bt-agent --capability=DisplayOnly -p pins", echo=True)
    if agent.expect("Default agent requested", timeout=10):
        print("No AGENT REGISTERED")
    else:
        print("agent spawned")
        print(agent.before)
    return agent

def wd_loop(agent):
    cond = True
    passkey = False
    uuid = False
    while cond == True:
        print("wd kick")
        if agent.expect("Passkey confirmed", timeout=60) and passkey==False:
            print("No device paired")
        else:
            print("passkey OK")
            passkey = True
            print(agent.before)
        if agent.expect("for UUID", timeout=60) and uuid == False:
            print("passkey confirmed but no device paired")
        else:
            print("UUID recovered")
            uuid = True
            print(agent.before)

def watchdog():
    agent = start_bt_agent()
    wd_loop(agent)
    print("exited WD")



