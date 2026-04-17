import app_control as phone
import random
import time
import display as video
import sound as audio
import threading
import shutil
import datetime
import os
from pytimedinput import timedKey
from pynput.keyboard import Key, Controller
import sys
import termios
import pathlib
import argparse
import cv2
import subprocess
from rest_piwigo import delete_image, send_to_slideshow, send_to_share, get_download_link
from share import get_qr_code
from simon_serial import setup_simon, read_from_serial, check_for_data, write_to_serial
from send_image import serve_banner, set_banner

# connect to phone to control it:
#   - start app
#   - loop over take photo
#   - pull gif and rename it.
num_pic = 15
num_gif = 0
gif_threshold = 10
local_path = ""


def show_image(path):
    img = cv2.imread(path)
    cv2.namedWindow("retour", cv2.WINDOW_NORMAL)
    cv2.imshow("retour",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def shuffle_list(liste):
    liste = list(range(1, 21))
    random.shuffle(liste)


def copy_to_gallery(num_gifs):
    for idx in range(0, num_gifs):
        filename = "gif" + str(idx) + ".gif"
        new_name = "gif" + str(datetime.datetime.utcnow()) + ".gif"
        shutil.copy2(f"{local_path}/" + filename,
                     f"{local_path}/showroom/images/" + new_name)


def copy_to_attachement(num_gifs):
    for idx in range(0, num_gifs):
        filename = "gif" + str(idx) + ".gif"
        shutil.copy2(f"{local_path}/" + filename,
                     f"{local_path}/public_html/images/" + filename)

def loop_phone():
    global num_gif
    gif = 0
    max_gif = 3
    waiting = True
    for gif in range(0, max_gif):
        for idx in range(0, num_pic):
            print("take photo ", idx)
            phone.take_photo(serial)
            time.sleep(delay_list[idx]/1000)
    time.sleep(3)
    for gif in range(0, max_gif):
        phone.pull_gif(serial, gif)
    # phone.erase_dir(serial)
    toggle_phone(serial, on=False)
    copy_to_attachement(3)
    copy_to_gallery(max_gif)
    waitKey("z")
    print("FIN")


def loop(ser):
    global num_gif
    gif = 0
    image_id=0
    max_gif = 1
    waiting = True
    share_gif=False
    write_to_serial(ser, 's')
    change_banner("images_web/3.png")
    time.sleep(1)
    change_banner("images_web/2.png")
    time.sleep(1)
    change_banner("images_web/1.png")
    time.sleep(1)
    change_banner("images_web/5_go.png")
    write_to_serial(ser, 'b')
    time.sleep(1)
    reset_banner()
    loading_gif()
    ret, frame = cam.read()
    for gif in range(0, max_gif):
        for idx in range(0, num_pic):
            print("take photo ", idx)
            ret, frame = cam.read()
            if ret:
                cv2.imwrite(f"tmp/Captured{idx}.png", frame)
            else:
                print("Could not take photo")
            time.sleep(delay_list[idx]/1000)
    time.sleep(1)
    subprocess.run("ffmpeg -y -framerate 10 -f image2 -i '/home/clem/Projets/perso/gif4000/tmp/Captured%d.png' -vf scale=918x691 output.gif", shell=True)
    for idx in range(0, num_pic):
        remove_file(f"tmp/Captured{idx}.png")
    time.sleep(1)
    out = False 
    while out == False:
        change_banner("images_web/6_choix.png")
        ser.reset_input_buffer()
        while not (check_for_data(ser)):
            time.sleep(0.5)
        key = read_from_serial(ser)

        print(key)
        if (key == "jaune"):
            change_banner("images_web/7_validation.png")
            write_to_serial(ser, 's')
            write_to_serial(ser, 'a')
            reset_qr_code()
            time.sleep(1)
            ser.reset_input_buffer()
            while not (check_for_data(ser)):
                time.sleep(1)
            key = read_from_serial(ser)

            if (key == "vert"):
                share_gif = True
                send_to_slideshow("output.gif")
                change_banner("images_web/8_banco.png")
                write_to_serial(ser, 's')
                write_to_serial(ser, 'b')
                time.sleep(1)
        elif(key == "vert"):
            image_id, url = send_to_share("output.gif")
            get_qr_code(url)
            change_qr_code()

        elif (key == "rouge"):
            change_banner("images_web/8_remerciement.png")
            reset_qr_code()
            reset_banner()
            time.sleep(1)
            out = True
        elif (key == "bleu"):
            change_banner("images_web/5_go.png")
            time.sleep(1)
            reset_banner()
            reset_qr_code()
            out = True

        else:
            print("FIN ITOU")
    if share_gif == False:
        delete_image(image_id)

    reset_qr_code()
    print("FIN LOOP")

def change_banner(banner_path):
    shutil.copy2(banner_path, "banner.png")

def change_qr_code():
    shutil.copy2("code.png", "qr.png")

def reset_qr_code():
    shutil.copy2("images_web/black.png", "qr.png")


def reset_banner():
    shutil.copy2("images_web/black.png", "banner.png")

def reset_gif():
    shutil.copy2("images_web/black.png", "output.gif")

def loading_gif():
    shutil.copy2("camera.gif", "output.gif")

def remove_file(path):
    try:
        os.remove(path)
    except:
        print("nothing to RM")


def toggle_phone(serial, on):
    if on == True and toggle_phone.phone_state == "starting":
        phone.toggle_screen(serial)
        phone.unlock_phone(serial)
        phone.unlock_phone(serial)
        phone.unlock_phone(serial)
        phone.start_app(serial)
        phone.stop_app(serial)
        phone.start_app(serial)
        toggle_phone.phone_state = "switched_on"
    if on == True and toggle_phone.phone_state == "switched_off":
        phone.toggle_screen(serial)
        phone.unlock_phone(serial)
        phone.unlock_phone(serial)
        phone.unlock_phone(serial)
        toggle_phone.phone_state = "switched_on"
    elif on == False and toggle_phone.phone_state == "switched_on":
        print("switching_on")
        phone.toggle_screen(serial)
        toggle_phone.phone_state = "switched_off"
    else:
        print("nothing to do with phone")


def init_randoms():
        # Generate random delays
    for num in range(0, num_pic):
        delay_list.append(random.randrange(100, 1000, 50))

    print(delay_list)
    track = 0

def wait4Keys(allowedkeys):
    waiting = True
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    ret_val = ""
    time.sleep(2)
    while waiting == True:
        print("Waiting for key")
        key, timeout = timedKey(timeout=5, allowCharacters=allowedkeys)
        if key == "a":
            ret_val = key
            waiting = False
        elif key == "b":
            ret_val = key
            waiting = False
        elif key == "c":
            ret_val = key
            waiting = False
        elif key == "d":
            ret_val = key
            waiting = False

        time.sleep(2)
        
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    return ret_val



def waitKey(exp_key):
    waiting = True
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    time.sleep(2)
    while waiting == True:
        print("Waiting for key")
        key, timeout = timedKey(timeout=5, allowCharacters=exp_key)
        print(exp_key)
        if key == exp_key:
            waiting = False
        time.sleep(2)
        
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)


parser = argparse.ArgumentParser(prog="gif4000", description="accidental gifomaton")
parser.add_argument("-p","--phone", action = "store_true")
is_phone = parser.parse_args().phone

if is_phone:
    toggle_phone.phone_state = "starting"
    serial = phone.connect_to_phone()

    if serial is None:
        print("serial is None, connect phone and relaunch")
        sys.exit(0)

    toggle_phone(serial, on=True)
else:
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)

delay_list = []
cond = False


local_path = pathlib.Path().resolve()
print(f"local path is {local_path}")

ser = setup_simon()
write_to_serial(ser, 's')
banner = 0
while cond == False:
    waiting = True
    init_randoms()
    reset_gif()
    reset_banner()
    reset_qr_code()
    while waiting == True:
        if (banner==0):
            change_banner("images_web/1_intro.png")
            write_to_serial(ser, 'a')
            banner=1
        if (check_for_data(ser)):
            line = read_from_serial(ser)
            if (line == "vert"):
                waiting = False
        time.sleep(0.5)

    reset_banner() 
    ser.flush()
    write_to_serial(ser, 's')
    if is_phone:
        loop_phone()
    else:
        loop(ser)
        banner=0

