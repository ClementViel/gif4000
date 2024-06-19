import app_control as phone
import random
import time
import display as video
import sound as audio
import threading
import bluetooth
import shutil
import datetime
import os
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

def copy_to_gallery():
    new_name = "gif" + str(datetime.datetime.utcnow()) + ".gif"
    shutil.copy2("/home/clem/Projets/gif4000/gif0.gif",
                 "/home/clem/Projets/gif4000/showroom/public/images/photos/" + new_name)

def copy_to_attachement():
    new_name = "gif" + str(datetime.datetime.utcnow()) + ".gif"
    shutil.copy2("/home/clem/Projets/gif4000/gif0.gif",
                 "/home/clem/Projets/gif4000/public_html/images/gif0.gif")


def loop(thread_audio):
    global num_gif
    waiting = True
    thread_audio.start()
    print("this is gif num ", num_gif)
    for idx in range(0, num_pic):
        print("take photo ", idx)
        phone.take_photo(serial)
        time.sleep(delay_list[idx]/1000)
    time.sleep(10)
    phone.pull_gif(serial, 0)
    phone.erase_dir(serial)
    audio_select("play", "partage", track)
    copy_to_attachement()
    while waiting == True:
        key, timeout = timedKey(timeout=5, allowCharacters="bsd")
        print(key)
        if key == "s" :
            copy_to_gallery()
        elif key == "d":
            waiting=False
    thread_audio.join()
    num_gif += 1

def remove_attachment(path):
    try:
        os.remove(path)
    except:
        print("nothing to RM")


def audio_accident(seq_array):
        for audio in seq_array:
            if  audio != 0:
                path = "/home/clem/Projets/gif4000/audio/" + audio
                audio.playSound(path)
            else:
                time.sleep(5)

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

# clean attachements
remove_attachment("/home/clem/Projets/gif4000/public_html/images/gif0.gif")
# Generate random delays
for num in range(0, num_pic):
    delay_list.append(random.randrange(300, 3000, 100))

print(delay_list)
#track = random.randint(0, 4)
track = 0
waiting = True
cond = False

# generation tableau séquence
sequence = ["ok1.mp3", 0, 0, 0, "ok2.mp3", 0, 0, 0, 0, "ok3.mp3"]
# generation du nombre d'accident
accident_num = random.randint(1,3)
# placement des accidents.
for index in range(accident_num):
        #tirage au sort du numéro de l'accident
        accident_idx = random.randint(0, 10)
        accident_place = random.choice([1, 2, 3, 6, 7, 8])
        print(accident_place)
        sequence[accident_place] = "/home/clem/Projets/gif4000/audio/accident" + str(accident_idx) + ".mp3"

print(sequence)
execution_audio = threading.Thread(target=audio_accident, args=(sequence))


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
    # TODO add a trigger
    loop(execution_audio)
    # TODO : make sure start/join is always working
    audio_select("play", "conclu", track)
