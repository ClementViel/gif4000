import app_control as phone
import random
import time
import display as video
import sound as audio
import threading
import bluetooth
import shutil
import datetime
from pytimedinput import timedKey
# connect to phone to control it:
#   - start app
#   - loop over take photo
#   - pull gif and rename it.
num_pic = 20
num_gif = 0


def shuffle_list(liste):
    liste = list(range(1, 21))
    random.shuffle(liste)


def loop():
    global num_gif
    waiting = True
    print("this is gif num ", num_gif)
    for idx in range(0, num_pic):
        print("take photo ", idx)
        phone.take_photo(serial)
        time.sleep(delay_list[idx]/1000)
    time.sleep(10)
    phone.pull_gif(serial, 0)
    phone.erase_dir(serial)
    new_name = "gif" + str(datetime.datetime.utcnow()) + ".gif"
    shutil.copy2("/home/clem/Projets/gif4000/gif0.gif",
                 "/home/clem/Projets/gif4000/showroom/public/images/photos/" + new_name)
    audio_select("play", "partage", track)
    while waiting == True:
        key, timeout = timedKey(timeout=5, allowCharacters="b")
        print(key)
        if key == "b":
            waiting = False

    bluetooth.bt_loop()
    num_gif += 1

def audio_select(function, moment, track):
    print("Thread audio starting")
    if function == "play":
        if moment == "intro":
            filename="intro" + str(track) +".mp3"
            path = "/home/clem/Projets/gif4000/audio/" + filename
        if moment == "explications":
            filename="exp" + str(track) +".mp3"
            path = "/home/clem/Projets/gif4000/audio/" + filename
        if moment == "exec":
            filename="exec" + str(track) +".mp3"
            path = "/home/clem/Projets/gif4000/audio/" + filename
        if moment == "partage":
            filename="partage" + str(track) +".mp3"
            path = "/home/clem/Projets/gif4000/audio/" + filename
        if moment == "conclu":
            filename="conclu" + str(track) +".mp3"
            path = "/home/clem/Projets/gif4000/audio/" + filename
        if moment == "attente":
            filename="attente" + str(track) +".mp3"
            path = "/home/clem/Projets/gif4000/audio/" + filename

        else:
            print("not the good sound")
        print("playing audio ",path)
        audio.playSound(path)

serial = phone.connect_to_phone()

if serial is None:
    print("serial is None, connect phone and relaunch")
    sys.exit(0)

delay_list = []
phone.turn_on_screen(serial)
phone.unlock_phone(serial)
phone.unlock_phone(serial)
phone.start_app(serial)
phone.stop_app(serial)
phone.start_app(serial)
# Generate random delays
for num in range(0, num_pic):
    delay_list.append(random.randrange(300, 3000, 100))

print(delay_list)
#track = random.randint(0, 4)
track = 0
waiting = True
cond = False
execution_audio = threading.Thread(target=audio_select, args=("play","exec",track ))


while cond == False:
    while waiting == True:
        audio_select("play", "attente", track)
        print("waiting for key")
        key, timeout = timedKey(timeout=5, allowCharacters="a")
        print(key)
        if key == "a":
            waiting = False
    waiting = True

    print("GIF4000 starting....press a")

    print(datetime.datetime.utcnow())


    print("START intro")
    audio_select("play", "intro", track)
    time.sleep(5)
    audio_select("play", "explications", track)

    execution_audio.start()
    loop()
    execution_audio.join()
    audio_select("play", "conclu", track)
